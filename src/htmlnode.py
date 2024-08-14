import functools

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def prop_to_html(self):
        def format_value(tup):
            return f"{tup[0]}=\"{tup[1]}\""
        return " ".join(map(format_value, self.props.items()))
    
    def __repr__(self):
        return f"HTMLNode({self.tag} {self.value} {self.children} {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str | None = None, props: dict | None = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self) -> str:
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"

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
        html_node = HTMLNode(props={"href": "haha", "a": "also ahaha", "target": "wasssup"})
        print(html_node)
        html_string = html_node.prop_to_html()
        print(html_string)
    except Exception as err:
        print(err)

    leaf_node = LeafNode(tag="p", value="This is a paragraph of text.")
    leaf_html_text = leaf_node.to_html()
    print(leaf_html_text)

if __name__ == "__main__":
    main()