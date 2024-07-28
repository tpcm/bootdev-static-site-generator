from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str | None = None, props: dict | None = None):
        super().__init__(tag, value, props)
    
    def to_html(self) -> str:
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"

def main():
    leaf_node = LeafNode(tag="p", value="This is a paragraph of text.")
    leaf_html_text = leaf_node.to_html()
    print(leaf_html_text)

if __name__ == "__main__":
    main()

