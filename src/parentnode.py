from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: list, props: dict | None = None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError()
        if not self.children:
            raise ValueError() 
        def apply_to_html(child):
            return child.to_html() 
        return f"<{self.tag}>" + "".join(map(apply_to_html, self.children)) + f"</{self.tag}>"
    

def main():
    try:
        parent_node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ]
        )
        print(parent_node.to_html())
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()