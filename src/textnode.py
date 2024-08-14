from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text: str, text_type: str, url: str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_text_node):
        if (self.text == other_text_node.text) \
            and (self.text_type == other_text_node.text_type) \
            and (self.url == other_text_node.url):
            return True
        return False
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(value=text_node.text, tag="b")
        case "italic":
            return LeafNode(value=text_node.text, tag="i")
        case "code":
            return LeafNode(value=text_node.text, tag="code")
        case "link":
            return LeafNode(value=text_node.text, tag="a", props={"href":text_node.url})
        case "image":
            return LeafNode(value="", tag="img", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("The text_type is not allowed")
    

def main():
    text_node = TextNode(text="HELLO WORLD", text_type="bold", url="haha.com")
    print(text_node)
    text_node_2 = TextNode(text="HELLO WORLD", text_type="bold", url="haha.cm")
    print(text_node == text_node_2)

    text_node_3 = TextNode(text="HELLO WORLD", text_type="bold", url=None)
    leaf_node = text_node_to_html_node(text_node_3)
    print(leaf_node)

if __name__ == "__main__":
    main()