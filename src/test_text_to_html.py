import unittest

from text_to_html import text_node_to_html_node
from textnode import TextNode
from leafnode import LeafNode

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode(text="HELLO WORLD", text_type="text", url=None)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, text_node.text)
        self.assertEqual(leaf_node.props, None)
    
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode(text="HELLO WORLD", text_type="bold", url=None)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, text_node.text)
        self.assertEqual(leaf_node.props, None)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode(text="HELLO WORLD", text_type="italic", url=None)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, text_node.text)
        self.assertEqual(leaf_node.props, None)

    def test_text_node_to_html_node_code(self):
        text_node = TextNode(text="HELLO WORLD", text_type="code", url=None)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, text_node.text)
        self.assertEqual(leaf_node.props, None)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode(text="HELLO WORLD", text_type="link", url="haha.com")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, text_node.text)
        self.assertEqual(leaf_node.props, {"href":"haha.com"})
    
    def test_text_node_to_html_node_image(self):
        text_node = TextNode(text="HELLO WORLD", text_type="image", url=None)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src":text_node.url, "alt":text_node.text})
    