import unittest

from leafnode import LeafNode

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



if __name__ == "__main__":
    unittest.main()
