import unittest

from textnode_delimiter import split_nodes_delimiter
from textnode import TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_text_type(self):
        text_type_text = "text"
        text_type_code = "code"

        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        self.assertIn(TextNode("This is text with a ", "text", None), new_nodes)
        self.assertIn(TextNode("code block", text_type_code, None), new_nodes)
        self.assertIn(TextNode(" word", "text", None), new_nodes)
    
    def test_bold_text_type(self):
        text_type_text = "text"
        text_type_bold = "bold"

        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        
        self.assertIn(TextNode("This is text with a ", "text", None), new_nodes)
        self.assertIn(TextNode("bold block", text_type_bold, None), new_nodes)
        self.assertIn(TextNode(" word", "text", None), new_nodes)
    
    def test_italic_text_type(self):
        text_type_text = "text"
        text_type_italic = "italic"

        node = TextNode("This is text with a *italic block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        
        self.assertIn(TextNode("This is text with a ", "text", None), new_nodes)
        self.assertIn(TextNode("italic block", text_type_italic, None), new_nodes)
        self.assertIn(TextNode(" word", "text", None), new_nodes)