import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_single_code_block(self):
        node = TextNode("Hello `code` world", TextType.Text)
        result = split_nodes_delimiter([node], "`", TextType.Code)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.Text),
            TextNode("code", TextType.Code),
            TextNode(" world", TextType.Text)
        ])

    def test_multiple_bold(self):
        node = TextNode("**bold** then **strong**", TextType.Text)
        result = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertEqual(result, [
            TextNode("bold", TextType.Bold),
            TextNode(" then ", TextType.Text),
            TextNode("strong", TextType.Bold)
        ])

    def test_italic_with_extra_text(self):
        node = TextNode("Start _emphasis_ end", TextType.Text)
        result = split_nodes_delimiter([node], "_", TextType.Italic)
        self.assertEqual(result, [
            TextNode("Start ", TextType.Text),
            TextNode("emphasis", TextType.Italic),
            TextNode(" end", TextType.Text)
        ])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is `broken", TextType.Text)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.Code)

    def test_non_text_node_untouched(self):
        node = TextNode("bold", TextType.Bold)
        result = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertEqual(result, [node])

if __name__ == "__main__":
    unittest.main()

