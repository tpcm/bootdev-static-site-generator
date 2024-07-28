import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq_success(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)
    
    def test_eq_success_with_url(self):
        node1 = TextNode("This is a text node", "bold", "haha.com")
        node2 = TextNode("This is a text node", "bold", "haha.com")
        self.assertEqual(node1, node2)

    def test_eq_fail(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node1, node2)

    def test_eq_fail_with_url(self):
        node1 = TextNode("This is a text node", "bold", "haha.com")
        node2 = TextNode("This is a different text node", "bold", "haha.co.uk")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()