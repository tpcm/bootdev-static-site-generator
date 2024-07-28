import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_success(self):
        html_node = HTMLNode(props={"href": "haha", "a": "also ahaha", "target": "wasssup"})
        html_string = html_node.prop_to_html()

        self.assertEqual(html_string, "href=\"haha\" a=\"also ahaha\" target=\"wasssup\"")

    def test_props_to_html_fail(self):
        html_node = HTMLNode(props={"href": "haha", "a": "also ahaha", "target": "wasssup"})
        html_string = html_node.prop_to_html()
        self.assertNotEqual(html_string, "href=haha a=also ahaha target=wasssup")

    def test_repr_eq(self):
        html_node = HTMLNode(tag="A", value="B", children=["A","B"], props={"href":"abc"})
        self.assertEqual(str(html_node), f"HTMLNode({html_node.tag} {html_node.value} {html_node.children} {html_node.props})")

if __name__ == "__main__":
    unittest.main()