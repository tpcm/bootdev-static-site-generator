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
    alt_text_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(alt_text_regex, text)

def extract_markdown_links(text: str):
    alt_text_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(alt_text_regex, text)

def split_nodes_link(old_nodes: list[str]):
    old_nodes_copy = old_nodes.copy()
    new_nodes = []

    for old_node in old_nodes_copy:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        links = extract_markdown_links(old_node_text)
        if not links:
            new_nodes.append(old_node)
            continue
        
        for link in links:
            sections = old_node_text.split(sep=f"[{link[0]}]({link[1]})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], text_type=text_type_text, url=None)
                )

            new_nodes.append(
                TextNode(link[0], text_type=text_type_link, url=link[1])
            )
            old_node_text = sections[1]
        if old_node_text != "":
            new_nodes.append(
                    TextNode(old_node_text, text_type=text_type_text, url=None)
                )

    return new_nodes

def split_nodes_image(old_nodes: list[str]):
    old_nodes_copy = old_nodes.copy()
    new_nodes = []

    for old_node in old_nodes_copy:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        images = extract_markdown_images(old_node_text)
        if not images:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = old_node_text.split(sep=f"![{image[0]}]({image[1]})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError("Invlid markdown, image not closed properly")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(text=sections[0], text_type=text_type_text, url=None)
                )
            
            new_nodes.append(
                TextNode(text=image[0], text_type=text_type_image, url=image[1])
            )
            old_node_text = sections[1]
        if old_node_text != "":
            new_nodes.append(
                TextNode(text=old_node_text, text_type=text_type_text, url=None)
            )
            
    return new_nodes

def text_to_textnodes(text) -> list:
    original_nodes = [
        TextNode(text=text, text_type=text_type_text, url=None)
    ]
    split_nodes = split_nodes_delimiter(old_nodes=original_nodes, delimiter="**", text_type=text_type_bold)
    split_nodes = split_nodes_delimiter(old_nodes=split_nodes, delimiter="*", text_type=text_type_italic)
    split_nodes = split_nodes_delimiter(old_nodes=split_nodes, delimiter="`", text_type=text_type_code)    
    split_nodes = split_nodes_image(old_nodes=split_nodes)
    split_nodes = split_nodes_link(old_nodes=split_nodes)
    return split_nodes



def main():    

    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))
if __name__ == "__main__":
    main()