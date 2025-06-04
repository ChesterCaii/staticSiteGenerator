import unittest
from textnode import TextNode, TextType
from converters import text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.Text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.Bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_link(self):
        node = TextNode("click here", TextType.Link, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.Image, "https://img.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://img.url", "alt": "Alt text"})

    def test_invalid_type(self):
        class FakeType:
            value = "unknown"
        node = TextNode("Some text", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()

