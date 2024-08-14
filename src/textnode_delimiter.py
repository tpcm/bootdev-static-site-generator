from textnode import TextNode

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

    

def main():    
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)

if __name__ == "__main__":
    main()