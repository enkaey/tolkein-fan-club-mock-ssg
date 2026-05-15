import unittest
from textnode import TextNode, TextType
from inline_markdown_parser import text_to_textnodes

class TestMarkdownParser(unittest.TestCase):
    def test_recursive_nested_formatting(self):
        #Testing custom recursive nesting engine
        text = "This **is _text_** with a `code block` _word_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is ", TextType.BOLD),
            TextNode("text", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
    
    def test_multiple_of_same_delimiter(self):
        # Verifies multiple non-nested instances of the same format
        text = "This is **bold1** and **bold2** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)
    
    def test_unclosed_delimiter_raises_error(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **unclosed bold text")
        
        with self.assertRaises(ValueError):
            text_to_textnodes("This is an unclosed italic sentence_")
    
    def test_empty_slices_skipped(self):
        # Ensures strings starting/ending with a delimiter don't create empty nodes

        text = "**Bold Start** normal _Italic End_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold Start", TextType.BOLD),
            TextNode(" normal ", TextType.TEXT),
            TextNode("Italic End", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
        self.assertTrue(all(node.text != "" for node in nodes))
    
    def test_starts_and_ends_with_tokens(self):
        # Edge case: checks what happens when tokens sit at the absolute boundary edges
        text = "![img](src)[link](href)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("img", TextType.IMG, "src"),
            TextNode("link", TextType.LINK, "href"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_full_mix(self):
        # A full mixture of links, images, code, bold, and italics in a single line
        text = "This is **bold** text with an ![image](https://boot.dev) and a [link](https://boot.dev) with `code` and _italics_"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("image", TextType.IMG, "https://boot.dev"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
    
    def test_multiple_images_and_links(self):
        # Verifies that the loop eats through multiple links/images consecutively
        text = "Check ![one](url1) and ![two](url2) or click [here](link1) or [there](link2)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("one", TextType.IMG, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMG, "url2"),
            TextNode(" or click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "link1"),
            TextNode(" or ", TextType.TEXT),
            TextNode("there", TextType.LINK, "link2"),
        ]
        self.assertEqual(nodes, expected)