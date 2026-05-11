import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click Here", {"href": "https://www.google.com", "alt": "this is a trial URL"})

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com" alt="this is a trial URL">Click Here</a>')
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just some plain text")
        self.assertEqual(node.to_html(), "Just some plain text")
    
    def test_to_html_no_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: no value")

    
    def test_repr(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(repr(node), "LeafNode('b', 'Bold text', None)")


if __name__ == "__main__":
    unittest.main()