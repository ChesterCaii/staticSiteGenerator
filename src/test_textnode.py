import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is not a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertNotEqual(node, node2)	
	
    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Italic)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.Bold, url="https://example.com")
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
