import unittest
from code import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks
)
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_bold(self):
        nodes = TextNode("**this is a bolded text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("this is a bolded text", TextType.BOLD)])

    def test_split_nodes_multiples(self):
        nodes = [TextNode("This is a node with _italic text_ in it", TextType.TEXT), TextNode("This is _another node_ with more _italic text_ in it", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a node with ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("another node", TextType.ITALIC),
            TextNode(" with more ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
            ])

    def test_invalid_markdown(self):
        node = TextNode("This has an unclosed `code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
        
    def test_no_split(self):
        node = TextNode("THIS IS AN _ITALIC_ IN A BOLD TEXT", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [node])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "For more information, read the [official documentation](https://example.com/docs) before continuing."
        )
        self.assertListEqual([("official documentation", "https://example.com/docs")], matches)

    def test_extract_both(self):
        images = extract_markdown_images("Check out this logo ![bootdev logo](https://example.com/logo.png) and visit [Boot.dev](https://www.boot.dev) for more info.")
        links = extract_markdown_links("Check out this logo ![bootdev logo](https://example.com/logo.png) and visit [Boot.dev](https://www.boot.dev) for more info.")
        self.assertEqual([("bootdev logo", "https://example.com/logo.png")], images)
        self.assertEqual([("Boot.dev", "https://www.boot.dev")], links)

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("no images here", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_single_image(self):
        node = TextNode("This is an ![image](https://i.imgur.com/zjjcJKZ.png) in a sentence", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in a sentence", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_link_single_link(self):
        node = TextNode("[boot](https://boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("boot", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)

    def test_split_no_links(self):
        node = TextNode("no links here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_split_link_multiple(self):
        node = TextNode(
            "[first link](https://example.com) is here and here is [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://example.com"),
                TextNode(" is here and here is ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_link_and_image(self):
        node = TextNode(
            "This has a link [to boot dev](https://www.boot.dev) and an image ![logo](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("This has a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an image ", TextType.TEXT),
                TextNode("logo", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_markdown_to_blocks_1(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                """- This is the first list item in a list block
- This is a list item
- This is another list item""",
            ],
            blocks
        )

    def test_markdown_to_blocks_2(self):
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

if __name__ == "__main__":
    unittest.main()