import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_single_attribute(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(tag="a", props={
            "href": "https://google.com",
            "target": "_blank"
        })
        result = node.props_to_html()
        self.assertIn('href="https://google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" "))
        self.assertEqual(len(result.split()), 2)

    def test_props_to_html_empty_props(self):
        node = HTMLNode(tag="p", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()

