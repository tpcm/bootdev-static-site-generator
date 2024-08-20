from loguru import logger
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    def strip_line(line):
        return line.strip()
    blocks = map(strip_line, blocks)
    return list(filter(None, blocks))

def block_to_block_type(block):
    if (
        block.startswith("# ")
        | block.startswith("## ")
        | block.startswith("### ")
        | block.startswith("#### ")
        | block.startswith("##### ")
        | block.startswith("###### ")
    ):
        return block_type_heading
    elif block[:3] + block[-3:] == "``````":
        return block_type_code
    
    lines = list(filter(None, block.split("\n")))
    def is_quote(lines):
        first_char = list(map(lambda x: True if x[0] == ">" else False, lines))
        return sum(first_char) == len(lines)
    
    def is_unordered_list(lines):
        first_char = list(map(lambda x: True if (x.startswith("* ")) | (x.startswith("- ")) else False, lines))
        return sum(first_char) == len(lines)
    
    def is_ordered_list(lines):
        counter = 1
        for line in lines:
            if line[:2] != f"{counter}.":
                return False
            counter+=1
        return True
    
    if is_quote(lines):
        return block_type_quote
    elif is_unordered_list(lines):
        return block_type_unordered_list
    elif is_ordered_list(lines):
        return block_type_ordered_list
    else:
        return block_type_paragraph

def get_heading_tag(block):
    if block.startswith("# "):
        return "h1"
    elif block.startswith("## "):
        return "h2"
    elif block.startswith("### "):
        return "h3"
    elif block.startswith("#### "):
        return "h4"
    elif block.startswith("##### "):
        return "h5"
    elif block.startswith("###### "):
        return "h6"
    else:
        raise ValueError("Too many # for heading section")

def get_block_tag(block_type: str) -> str:
    match block_type:
        case "quote":
            return "blockquote"
        case "unordered_list":
            return "ul"
        case "ordered_list":
            return "ol"
        case block_type_code:
            return block_type_code

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))

def apply_nested_tag_to_list_item(child_node):
    return ParentNode(
        tag="li",
        children=[child_node]
    )

def heading_to_html(block):
    if not block.startswith("#"):
        raise ValueError("Invalid heading block")
    tag = get_heading_tag(block)
    num_hashtag = int(tag[-1])
    block = block[num_hashtag+1:]
    child_nodes = text_to_children(block)
    return ParentNode(
                tag=tag,
                children=child_nodes
            )

def code_to_html(block):
    if not block.startswith("```") and not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    block = " ".join(block[3:-3].split("\n"))
    child_nodes = text_to_children(text=block)
    return ParentNode(
            tag="pre",
            children=[ParentNode(
                tag="code",
                children=child_nodes
            )]
        )

def quote_to_html(block):
    lines = list(filter(None, block.split("\n", )))
    # logger.debug(lines)
    stripped_quote = list(filter(None, map(lambda x: x.lstrip(">").strip() if x[0] == ">" else None, lines)))
    # logger.debug(stripped_quote)
    if len(stripped_quote) != len(lines):
        raise ValueError("Invalid quote block")
    block = " ".join(stripped_quote)
    child_nodes = text_to_children(text=block)
    return ParentNode(
        tag="blockquote",
        children=child_nodes
    )

def paragraph_to_html(block):
    child_nodes = text_to_children(" ".join(block.split("\n")))
    return ParentNode(
        tag="p",
        children=child_nodes
    )

def unordered_list_to_html(block):
    lines = block.split("\n")
    # logger.debug(lines)
    is_ul = list(filter(None, map(lambda x: x[2:].strip() if (x.startswith("* ")) | (x.startswith("- ")) else None, lines)))
    # logger.debug(is_ul)
    if len(is_ul) != len(lines):
        raise ValueError("Invalid unordered list block")
    child_nodes = [
        ParentNode(
            tag="li",
            children=text_to_children(child)
        ) for child in is_ul
    ]
    return ParentNode(
                tag="ul",
                children=child_nodes
            )

def ordered_list_to_html(block):
    lines = block.split("\n")
    child_nodes = []
    counter = 1
    for line in lines:
        if line[:2] != f"{counter}.":
            raise ValueError("Invalid ordered list block")
        counter+=1
        # logger.info(line)
        text = line[2:].strip()
        # logger.info(text)
        child_nodes.append(
            ParentNode(
                tag="li",
                children=text_to_children(text)
            )
        )
    return ParentNode(
                tag="ol",
                children=child_nodes
            )

def block_to_html_node(block):
    block_type = block_to_block_type(
            block=block
        )
    if block_type == block_type_heading:
        return heading_to_html(block)
    elif block_type == block_type_quote:
        return quote_to_html(block)
    elif block_type == block_type_code:
        return code_to_html(block)
    elif block_type == block_type_paragraph:
        return paragraph_to_html(block)
    elif block_type == block_type_unordered_list:
        return unordered_list_to_html(block)
    elif block_type == block_type_ordered_list:
        return ordered_list_to_html(block)
    return ValueError("Invalid block type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(
        markdown=markdown
    )
    block_html_nodes = []
    for block in blocks:
        block_html_nodes.append(block_to_html_node(block))
    return ParentNode(
        tag="div",
        children=block_html_nodes
    )

def main():
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
    html_nodes = markdown_to_html_node(markdown)
    print(html_nodes)

if __name__ == "__main__":
    main()