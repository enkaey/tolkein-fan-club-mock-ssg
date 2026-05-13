import unittest
from textnode import TextNode, TextType
from markdown_parser import text_to_textnodes

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