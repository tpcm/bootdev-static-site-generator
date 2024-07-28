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

    
