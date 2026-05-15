import unittest
from block_markdown_parser import markdown_to_blocks

class TestBlockMarkdownParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_excess_newlines(self):
        # Test extreme whitespace separation between paragraphs
        md = "Paragraph 1\n\n\n\nParagraph 2\n\n\nParagraph 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1", "Paragraph 2", "Paragraph 3"])

    def test_markdown_to_blocks_whitespace_lines(self):
        # Test blank lines that contain hidden spaces or tabs
        md = "Paragraph 1\n\n  \t  \n\nParagraph 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1", "Paragraph 2"])
