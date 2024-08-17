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
        first_char = list(map(lambda x: True if (x[0] == "*") | (x[0] == "-") else False, lines))
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
        children=child_node
    )

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(
        markdown=markdown
    )
    block_html_nodes = []
    for block in blocks:
        child_nodes = text_to_children(block)
        block_type = block_to_block_type(
            block=block
        )
        if block_type == block_type_code:
            block_html_node = ParentNode(
            tag="pre",
            children=ParentNode(
                tag=get_block_tag(block_type),
                children=child_nodes
            )
        )
        elif block_type == block_type_heading:
            block_html_node = ParentNode(
                tag=get_heading_tag(block),
                children=child_nodes
            )
        elif (block_type == block_type_unordered_list) | (block_type == block_type_ordered_list):
            block_html_node = ParentNode(
                tag=get_block_tag(block_type),
                children=list(map(apply_nested_tag_to_list_item, child_nodes))
            )
        else:
            block_html_node = ParentNode(
                tag=get_block_tag(block_type),
                children=child_nodes
            )
        block_html_nodes.append(block_html_node)
    return ParentNode(
        tag="div",
        children=block_html_nodes
    )

def main():
#     markdown = """# This is a heading

# This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# * This is the first list item in a list block
# * This is a list item
# * This is another list item"""

#     print(markdown_to_html_node(markdown))
    markdown = "# This is a heading\n\nThis is a paragraph of text. It has some words inside of it."
    html_nodes = markdown_to_html_node(markdown)
    print(html_nodes)
    print(ParentNode(
        tag="div",
        children=[
            ParentNode(
                tag="h1",
                children=[LeafNode(value="# This is a heading")]
            ),
            ParentNode(
                tag="paragraph",
                children=[LeafNode(value="This is a paragraph of text. It has some words inside of it.")]
            )
        ]
    ))

if __name__ == "__main__":
    main()