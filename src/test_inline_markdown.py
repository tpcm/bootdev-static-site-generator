import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images
)

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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_valid_image_success(self):
        image_text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) \
            and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(
            extract_markdown_images(image_text),
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif)'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg)')
            ]
        )

    def test_extract_invalid_image_fail(self):
        link_text = ("This is text with a link [to boot dev](https://www.boot.dev) \
            and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(
            extract_markdown_images(link_text),
            []
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_valid_link_success(self):
        link_text = ("This is text with a link [to boot dev](https://www.boot.dev) \
            and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(
            extract_markdown_links(link_text),
            [
                ('to boot dev', 'https://www.boot.dev)'),
                ('to youtube', 'https://www.youtube.com/@bootdotdev)')
            ]
        )

    def test_extract_invalid_link_fail(self):
        image_text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) \
            and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(
            extract_markdown_links(image_text),
            []
        )