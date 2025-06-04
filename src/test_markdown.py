import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "![first](url1) and ![second](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "url1"), ("second", "url2")], matches)

    def test_extract_markdown_links(self):
        text = "This is a [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_images_not_matched_as_links(self):
        text = "![alt](img.png) and [text](url.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("alt", "img.png")], image_matches)
        self.assertListEqual([("text", "url.com")], link_matches)
def test_text_to_textnodes(self):
    text = (
        "This is **text** with an _italic_ word and a `code block` and an "
        "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
        "[link](https://boot.dev)"
    )

    expected = [
        TextNode("This is ", TextType.Text),
        TextNode("text", TextType.Bold),
        TextNode(" with an ", TextType.Text),
        TextNode("italic", TextType.Italic),
        TextNode(" word and a ", TextType.Text),
        TextNode("code block", TextType.Code),
        TextNode(" and an ", TextType.Text),
        TextNode("obi wan image", TextType.Image, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.Text),
        TextNode("link", TextType.Link, "https://boot.dev"),
    ]

    self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()

