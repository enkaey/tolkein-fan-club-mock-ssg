from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def count_nodes(self, node):
        if not node.children:
            return 1
        return 1 + sum(self.count_nodes(child) for child in node.children)
    
    def test_recursive_count(self):
        #Create a tree with 4 nested nodes
        grandchildren = [HTMLNode("p", "This should be #4.")]
        children = [HTMLNode("span", "This should be #2.", None),
                    HTMLNode("div", None, grandchildren)]
        tree = HTMLNode("h2", "#1 Will the count work?", children)

        self.assertEqual(self.count_nodes(tree), 4)
    
    def test_children_init(self):
        child = HTMLNode("span", "This is a child", None)
        parent = HTMLNode("h1", "This is a parent", [child])
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].tag, "span")
    
    def test_nested_children(self):
        grandchildren = [HTMLNode("p", "Grandchild.")]
        children = [HTMLNode("span", "I'm the uncle.", None),
                    HTMLNode("div", "I'm the parent.", grandchildren)]
        tree = HTMLNode("h2", "I'm the grandparent.", children)

        self.assertEqual(tree.children[1].children[0].value, "Grandchild.")
        self.assertNotEqual(tree.children[0].value, "I'm the parent.")
    
    def test_repr(self):
        expected = "HTMLNode('a', 'Click Here', children: None, {'href': 'https://www.google.com', 'target': '_blank'})"

        node = repr(HTMLNode("a", "Click Here", None, {"href": "https://www.google.com", "target": "_blank"}))

        self.assertEqual(node, expected)
    
    def test_props_to_html(self):
        node = HTMLNode("a", "Click Here", None, {"href": "https://www.google.com", "target": "_blank"})

        props = node.props_to_html()

        self.assertEqual(props, ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()