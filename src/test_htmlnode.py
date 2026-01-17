import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_attributes(self):
        node1 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        test1 = node1.props_to_html()
        solution1 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(test1, solution1)
    
    def test_props_to_html_empty_dict(self):
        node2 = HTMLNode(props={})
        test2 = node2.props_to_html()
        solution2 = ""
        self.assertEqual(test2, solution2)

    def test_htmlnode_constructor_sets_fields(self):
        children = [HTMLNode(tag="span", value="hi")]
        node = HTMLNode(tag="a", value="link", children=children, props={"href": "https://example.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props["href"], "https://example.com")

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_constructor(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link")
        self.assertEqual(node.props["href"], "https://example.com")

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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_b(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_text_i(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_text_a(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_text_img(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://example.com/bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/bear.png")
        self.assertEqual(html_node.props["alt"], "This is an image text node")


if __name__ == "__main__":
    unittest.main()