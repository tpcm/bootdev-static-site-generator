import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_to_html_eq(self):
        leaf_node = LeafNode(tag="p", value="This is a paragraph of text.")
        leaf_html_text = leaf_node.to_html()
        self.assertEqual(leaf_html_text, "<p>This is a paragraph of text.</p>")

    def test_to_html_not_eq(self):
        leaf_node = LeafNode(tag="p", value="This is not a paragraph of text.")
        leaf_html_text = leaf_node.to_html()
        self.assertNotEqual(leaf_html_text, "<p>This is a paragraph of text.</p>")

    
    def test_to_html_raise_value_error(self):
        leaf_node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_no_tag(self):
        leaf_node = LeafNode(value="This is not a paragraph of text.")
        self.assertEqual(leaf_node.to_html(), leaf_node.value)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_just_leafnodes(self):
        parent_node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ]
        )
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_parentnode_with_leafnodes(self):
        parent_node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag="a",
                    children=[
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(tag=None, value="Normal text"),
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ]
                )
            ]
        )
        self.assertEqual(parent_node.to_html(), "<p><a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a></p>")

    def test_to_html_with_two_parentnodes_with_leafnodes(self):
        parent_node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag="a",
                    children=[
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(tag=None, value="Normal text"),
                    ]
                ),
                ParentNode(
                    tag="z",
                    children=[
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ]
                )
            ]
        )
        self.assertEqual(parent_node.to_html(), "<p><a><b>Bold text</b>Normal text</a><z><i>italic text</i>Normal text</z></p>")

    def test_to_html_no_tag_raises_value_error(self):
        parent_node = ParentNode(
            tag=None,
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ]
        )
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_no_children_raises_value_error(self):
        parent_node = ParentNode(
            tag=None,
            children=[]
        )
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_two_parentnodes_with_no_children_raises_valu_error(self):
        parent_node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag="a",
                    children=[]
                ),
                ParentNode(
                    tag="z",
                    children=[]
                )
            ]
        )
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_two_parentnodes_with_children_no_tags_raises_valu_error(self):
        parent_node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag=None,
                    children=[
                        LeafNode(tag="i", value="italic text"),
                ]
                ),
                ParentNode(
                    tag=None,
                    children=[
                        LeafNode(tag=None, value="Normal text")
                    ]
                )
            ]
        )
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()