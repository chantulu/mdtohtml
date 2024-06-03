import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", "bold", "https://google.com")
        node2 = TextNode("This is a text node", "bold", "https://google.com")
        self.assertEqual(node, node2)
        node = TextNode("This is a text node 1", "bold", "https://google.com")
        node2 = TextNode("This is a text node 2", "bold", "https://google.com")
        self.assertNotEqual(node, node2)

class TestTextNodeAttr(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node with url", "bold", "https://google.com")
        self.assertTrue(hasattr(node, "url"), msg='obj lacking an attribute. obj: %s, intendedAttr: %s' % (node, "url"))

if __name__ == "__main__":
    unittest.main()