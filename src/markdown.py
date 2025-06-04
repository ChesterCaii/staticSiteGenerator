from textnode import TextNode, TextType

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

