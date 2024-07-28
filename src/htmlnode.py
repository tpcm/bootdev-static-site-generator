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
        
    
def main():
    try:
        html_node = HTMLNode(props={"href": "haha", "a": "also ahaha", "target": "wasssup"})
        print(html_node)
        html_string = html_node.prop_to_html()
        print(html_string)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()