import re
from textnode import TextNode, TextType
import unittest
from markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.Text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # Delimiters should be even: text, delimited, text, delimited, ...
        if len(parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter '{delimiter}' in: '{node.text}'")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.Text))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only operate on plain text nodes
        if node.text_type != TextType.Text:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            split_parts = text.split(f"![{alt}]({url})", 1)
            before, text = split_parts[0], split_parts[1]

            if before.strip() != "":
                new_nodes.append(TextNode(before, TextType.Text))
            new_nodes.append(TextNode(alt, TextType.Image, url))

        if text.strip() != "":
            new_nodes.append(TextNode(text, TextType.Text))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.Text:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for label, url in links:
            split_parts = text.split(f"[{label}]({url})", 1)
            before, text = split_parts[0], split_parts[1]

            if before.strip() != "":
                new_nodes.append(TextNode(before, TextType.Text))
            new_nodes.append(TextNode(label, TextType.Link, url))

        if text.strip() != "":
            new_nodes.append(TextNode(text, TextType.Text))

    return new_nodes

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.Text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Text),
                TextNode("image", TextType.Image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.Text),
                TextNode("second image", TextType.Image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Go [home](https://home.com) or [search](https://google.com)",
            TextType.Text
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go ", TextType.Text),
                TextNode("home", TextType.Link, "https://home.com"),
                TextNode(" or ", TextType.Text),
                TextNode("search", TextType.Link, "https://google.com"),
            ],
            new_nodes
        )

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.Text)]

    # Apply the splitters in order: images, links, code, bold, italic
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.Code)
    nodes = split_nodes_delimiter(nodes, "**", TextType.Bold)
    nodes = split_nodes_delimiter(nodes, "_", TextType.Italic)

    return nodes
