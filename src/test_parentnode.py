import unittest

from parentnode import ParentNode
from leafnode import LeafNode 

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