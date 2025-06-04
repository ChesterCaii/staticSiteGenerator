from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.Text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.Bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.Italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.Code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.Link:
        if not text_node.url:
            raise ValueError("Link TextNode requires a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.Image:
        if not text_node.url:
            raise ValueError("Image TextNode requires a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")

