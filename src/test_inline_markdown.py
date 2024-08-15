import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_link,
    split_nodes_image
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_text_type(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        self.assertIn(TextNode("This is text with a ", "text", None), new_nodes)
        self.assertIn(TextNode("code block", text_type_code, None), new_nodes)
        self.assertIn(TextNode(" word", "text", None), new_nodes)
    
    def test_bold_text_type(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        
        self.assertIn(TextNode("This is text with a ", "text", None), new_nodes)
        self.assertIn(TextNode("bold block", text_type_bold, None), new_nodes)
        self.assertIn(TextNode(" word", "text", None), new_nodes)
    
    def test_italic_text_type(self):
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
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
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
                ('to boot dev', 'https://www.boot.dev'),
                ('to youtube', 'https://www.youtube.com/@bootdotdev')
            ]
        )

    def test_extract_invalid_link_fail(self):
        image_text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) \
            and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(
            extract_markdown_links(image_text),
            []
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_success_1_link(self):
        node = TextNode(
            "This is text with an image after a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with an image after a link ![to boot dev](https://www.boot.dev) and ",
                    text_type_text
                ),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )
    def test_split_nodes_link_success_2_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )
    def test_split_nodes_link_invalid(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [node]
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_success_just_image(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "to boot dev", text_type_image, "https://www.boot.dev"
                ),
            ]
        )


    def test_split_nodes_image_success_1_image(self):
        node = TextNode(
            ("This is text with an image after a link [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"),
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with an image after a link [rick roll](https://i.imgur.com/aKaOqIh.gif) and ",
                    text_type_text
                ),
                TextNode(
                    "obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ]
        )
    def test_split_nodes_image_success_2_images(self):
        node = TextNode(
            ("This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"),
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image ", text_type_text),
                TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ]
        )
    def test_split_nodes_image_success_just_image(self):
        node = TextNode(
            ("![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"),
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ]
        )
    
    def test_split_nodes_image_invalid(self):
        node = TextNode(
            ("This is text with an image [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"),
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [node]
        )