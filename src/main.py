from textnode import TextNode, TextType

print("hello world")
def main():
	node = TextNode("This is some **bold** text", TextType.Bold)
	print(node)
main()
