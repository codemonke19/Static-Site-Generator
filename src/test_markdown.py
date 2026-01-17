import unittest
from markdown import block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestBlockToBlockType(unittest.TestCase):
    def test_block_type_heading(self):
        block = "# My Title"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_type_code(self):
        block = "```\nprint('hi')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_type_quote(self):
        block = "> line one\n> line two"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_type_ol(self):
        block = "1. first\n2. second\n3. third"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_type_ul(self):
        block = "- item one\n- item two"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_type_paragraph(self):
        block = "Just a normal paragraph of text."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_to_htmlnode_p(self):
        markdown = "This is **bold** text\n\nAnother paragraph"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><p>This is <b>bold</b> text</p><p>Another paragraph</p></div>",
            )

    def test_markdown_to_htmlnode_heading(self):
        markdown = "# Title"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Title</h1></div>")

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = "> quoted _text_ here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quoted <i>text</i> here</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- one\n- two with **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two with <b>bold</b></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second with _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second with <i>italic</i></li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()