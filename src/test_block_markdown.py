import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from test_htmlnode import ParentNode, LeafNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(markdown=markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                
            ]
        )
    
    def test_markdown_to_block_one_line(self):
        markdown = """# This is a heading"""
        blocks = markdown_to_blocks(markdown=markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
            ]
        )
    def test_markdown_to_block_empty_lines_after(self):
        markdown = """# This is a heading
        
        
        
        
        """
        blocks = markdown_to_blocks(markdown=markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
            ]
        )
    def test_markdown_to_block_empty_lines_before(self):
        markdown = """
        
        
        
        
        # This is a heading"""
        blocks = markdown_to_blocks(markdown=markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = """This is the first list item in a list block
This is a list item
This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "paragraph"
        )
    def test_unordered_list(self):
        block = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "unordered_list"
        )
    def test_ordered_list(self):
        block = """1.This is the first list item in a list block
2.This is a list item
3.This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "ordered_list"
        )
    def test_ordered_list_invalid(self):
        block = """1.This is the first list item in a list block
4.This is a list item
3.This is another list item"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(
            block_type,
            "ordered_list"
        )
        self.assertEqual(
            block_type,
            "paragraph"
        )
    def test_heading(self):
        block = """# Heading"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "heading"
        )
    def test_code(self):
        block = """```Code```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "code"
        )
    def test_quote(self):
        block = """>quote"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "quote"
        )
    def test_multi_quote(self):
        block = """>quote\n>quote\n>quote"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            "quote"
        )

class TestMarkdownToHtml(unittest.TestCase):
    def test_small_markdown_success(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some words inside of it."
        html_nodes = markdown_to_html_node(markdown)
        self.assertEqual(
            str(html_nodes),
            str(ParentNode(
                tag="div",
                children=[
                    ParentNode(
                        tag="h1",
                        children=[LeafNode(value="# This is a heading")]
                    ),
                    ParentNode(
                        tag="paragraph",
                        children=[LeafNode(value="This is a paragraph of text. It has some words inside of it.")]
                    )
                ]
            ))
        )