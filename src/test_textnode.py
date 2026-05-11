import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_other = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node_other)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_other = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node_other)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK,)
        node_other = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node_other)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
        self.assertEqual("TextNode('This is a text node', `, 'https://boot.dev')", repr(node))

if __name__ == "__main__":
    unittest.main()