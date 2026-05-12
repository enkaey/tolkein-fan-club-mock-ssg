import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "bold")])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    #Deeply Nested Siblings
    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold"),
                ParentNode("span", [LeafNode("i", "italic")]),
                LeafNode(None, "plain"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold</b><span><i>italic</i></span>plain</h2>"
        )     
    