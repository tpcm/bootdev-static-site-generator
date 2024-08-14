import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)


def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: str
) -> list[TextNode]:
    
    old_nodes_copy = old_nodes.copy()
    new_nodes = []

    def split_node_text(node):
        return node.text.split(delimiter)
    
    
    for old_node in old_nodes_copy:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        parts = split_node_text(old_node)
        for ind, part in enumerate(parts):
            if ind % 2 == 0:
                if part:  # Only add non-empty parts
                        new_nodes.append(TextNode(part, "text"))
            else:
                # It's a delimiter type node part
                if part:  # Only add non-empty parts
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text: str):
    alt_text_regex = r"\!\[(.*?)\]\((.*?\))"
    return re.findall(alt_text_regex, text)

def extract_markdown_links(text: str):
    alt_text_regex = r"[^!]\[(.*?)\]\((.*?\))"
    return re.findall(alt_text_regex, text)

    

def main():    
    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    print(new_nodes)

    image_text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) \
            and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
    print(extract_markdown_images(image_text))
    print(extract_markdown_links(image_text))
    
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_images(link_text))
    print(extract_markdown_links(link_text))

if __name__ == "__main__":
    main()