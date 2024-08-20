import os
import pathlib
import shutil
from loguru import logger

from block_markdown import markdown_to_html_node

def clear_dir(dir_path):
    dir_contents = list(map(lambda x: dir_path / x, os.listdir(dir_path)))
    if not dir_contents:
        return True
    for content_path in dir_contents:
        if os.path.isfile(content_path):
            os.remove(content_path)
        elif os.path.isdir(content_path):
            shutil.rmtree(content_path)
    return True

def copy_static_to_public(src_dst_paths):
    if not src_dst_paths:
        return True
    src_dst_paths_copy = src_dst_paths.copy()
    for src_path, dst_path in src_dst_paths_copy:
        logger.info(src_path)
        if os.path.isfile(src_path):
            shutil.copy(src=src_path, dst=dst_path)
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            logger.info("creating dir")
            next_level = list(map(lambda x: (src_path / x, dst_path / x), os.listdir(src_path)))
            if not next_level:
                logger.info("finished")
                return True
            logger.info("going down")
            copy_static_to_public(next_level)
    return True

def extract_title(markdown):
    header = markdown.split("\n")[0]
    if not markdown.startswith("# "):
        raise ValueError("Invalid h1 header")
    header = header.lstrip("# ").strip()
    return header

def generate_page(from_path, template_path, dest_path):
    # logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    # logger.info(markdown)
    page_html_node = markdown_to_html_node(markdown=markdown)
    page_html = page_html_node.to_html()
    title = extract_title(markdown=markdown)
    with open(template_path, "r") as f:
        template = f.read()
    # logger.info(template)
    new_template = template.replace("{{ Title }}", title)
    new_template = new_template.replace("{{ Content }}", page_html)
    with open(dest_path, "w") as f:
        f.write(new_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src_dst_paths = list(map(lambda x: (dir_path_content / x, dest_dir_path / x.replace(".md", ".html")), os.listdir(dir_path_content)))
    logger.debug(f"content paths: {src_dst_paths}")
    for content in src_dst_paths:
        if not os.path.isfile(content[0]):
            if not os.path.exists(content[1]):
                os.mkdir(content[1])
            generate_pages_recursive(content[0], template_path, content[1])
        else:
            logger.debug(f"writting to {content[1]}")
            generate_page(from_path=content[0], template_path=template_path, dest_path=content[1])
    return True

def main():
    cwd = pathlib.Path(os.getcwd())
    clear_dir(dir_path=(cwd / "public"))

    public_path = cwd / "public"
    static_path = cwd / "static"
    src_dst_paths = list(map(lambda x: (static_path / x, public_path / x), os.listdir(static_path)))
    copy_static_to_public(src_dst_paths)

    from_path = cwd / "content"
    template_path = cwd / "template.html"
    dest_path = cwd / "public"

    generate_pages_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()

