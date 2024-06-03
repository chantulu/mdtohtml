import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_vals(self):
        node = HTMLNode("a","hi")
        self.assertTrue(node.tag == "a", "Node tag contains no expected \"a\"")
        self.assertTrue(node.value == "hi", "Node value contains no expected \"hi\"")
        child_node = HTMLNode("a","hi",None,{"href": "https://www.google.com"})
        node = HTMLNode("div",None,[child_node],None)
        self.assertIn("{'a': 1}",repr(node),"Node contains no (a) children, expected 1")
        self.assertIn("tag:div",repr(node),"Node contains no valid tag, expected div")
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

class TestLeafNode(unittest.TestCase):
    def test_vals(self):
        node = LeafNode("a","hi")
        self.assertTrue(node.tag == "a", "Node tag contains no expected \"a\"")
        self.assertTrue(node.value == "hi", "Node value contains no expected \"hi\"")
        node = LeafNode("div","hello",None)
        self.assertIn("tag:div",repr(node),"Node contains no valid tag, expected div")
    def test_to_html_props(self):
        node = LeafNode(
            "div",
            "Hello, world!",
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
    def to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

class TestParentNode(unittest.TestCase):
    def test_ret(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
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


if __name__ == "__main__":
    unittest.main()