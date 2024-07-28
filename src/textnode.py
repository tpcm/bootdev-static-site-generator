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
    
def main():
    text_node = TextNode(text="HELLO WORLD", text_type="bold", url="haha.com")
    print(text_node)
    text_node_2 = TextNode(text="HELLO WORLD", text_type="bold", url="haha.cm")
    print(text_node == text_node_2)

if __name__ == "__main__":
    main()