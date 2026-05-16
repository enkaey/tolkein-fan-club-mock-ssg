import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMDToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node_integration(self):
        # 1. A complex mix of every single block type with inline styles
        md = """
# Heading Level 1

This is a **bold** paragraph with `code` inline.

```
print("Hello from code block")
```

> This is a multi-line quote
> that should stitch together cleanly.

- Unordered item 1
- Unordered item 2 with _italics_

1. First ordered step
2. Second ordered step
"""
        html_tree = markdown_to_html_node(md)
        raw_html = html_tree.to_html()

        # Verify parent structure
        self.assertTrue(raw_html.startswith("<div>"))
        self.assertTrue(raw_html.endswith("</div>"))

        # Verify individual block transformations
        # 1.1. Header
        self.assertIn("<h1>Heading Level 1</h1>", raw_html)

        # 1.2. Paragraph with inline elements
        self.assertIn(
            "<p>This is a <b>bold</b> paragraph with <code>code</code> inline.</p>", raw_html
            )
        
        # 1.3. Preformatted code block
        self.assertIn(
            '<pre><code>print("Hello from code block")</code></pre>', raw_html
            )
        
        # 1.4. Multi-line quote
        self.assertIn(
            "<blockquote>This is a multi-line quote that should stitch together cleanly.</blockquote>", raw_html
            )
        
        # 1.5. Unordered List
        self.assertIn(
            "<ul><li>Unordered item 1</li><li>Unordered item 2 with <i>italics</i></li></ul", raw_html
            )
        
        # 1.6. Ordered List
        self.assertIn(
            "<ol><li>First ordered step</li><li>Second ordered step</li></ol>", raw_html
            )
    
    def test_fallback_to_paragraph(self):
        # 2. Ensures that if a block defaults to a PARAGRAPH, the loop handles it safely
        md = "###NoSpaceHeading Here"
        html_tree = markdown_to_html_node(md)
        raw_html = html_tree.to_html()

        # Should wrap a broken heading in a paragraph tag, not an h3 tag
        self.assertEqual("<div><p>###NoSpaceHeading Here</p></div>", raw_html)
    
    def test_empty_document(self):
        # 3. Edge case: what if the markdown document is completely empty or just spaces?
        md = "   \n\n   "
        html_tree = markdown_to_html_node(md)
        raw_html = html_tree.to_html()
        
        # Should just return an empty wrapping div
        self.assertEqual("<div></div>", raw_html)