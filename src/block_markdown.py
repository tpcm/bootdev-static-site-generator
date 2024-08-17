from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    def strip_line(line):
        return line.strip()
    blocks = map(strip_line, blocks)
    return list(filter(None, blocks))

def block_to_block_type(block):
    if block[:2] == "# ":
        return "heading"
    elif block[:3] + block[-3:] == "``````":
        return "code"
    
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
        return "quote"
    elif is_unordered_list(lines):
        return "unordered_list"
    elif is_ordered_list(lines):
        return "ordered_list"
    else:
        return "paragraph"

def main():
    block = ">quote"
    def is_quote():
        lines = list(filter(None, block.split("\n")))
        first_char = [True for line in lines if line[0] == ">"]
        print(first_char)
        return sum(first_char) == len(lines)
    print(is_quote())

if __name__ == "__main__":
    main()