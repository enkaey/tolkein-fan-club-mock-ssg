import unittest
from textnode_to_html_node import text_node_to_html_node
from textnode import TextNode, TextType

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is plain text")

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMG, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://boot.dev", "alt": "This is alt text"},
        )
        # Testing the self-closing logic
        self.assertEqual(html_node.to_html(), '<img src="https://boot.dev" alt="This is alt text">')

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://google.com"})
