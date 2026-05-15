import unittest
from block_markdown_parser import BlockType, markdown_to_blocks, block_to_block_type

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

    def test_heading_success(self):
        self.assertEqual(block_to_block_type("### Valid Heading"), BlockType.HEADING)

    def test_broken_quote(self):
        # Line 2 is missing the '>' marker, should default to paragraph
        broken_quote = "> This is line 1\nThis is line 2 without marker"
        self.assertEqual(block_to_block_type(broken_quote), BlockType.PARAGRAPH)

    def test_ordered_list_broken_sequence(self):
        # Sequence jumps from 1 to 3, should fail validation
        broken_list = "1. Item one\n3. Broken item two"
        self.assertEqual(block_to_block_type(broken_list), BlockType.PARAGRAPH)
        
    def test_code_block(self):
        code = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)