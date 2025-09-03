import unittest

from textnode import DelimiterType, TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_defaults(self):
        node = TextNode("Test", TextType.LINK)
        node2 = TextNode("Test", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://www.test.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_text(self):
        node = TextNode("This is a **string** value with an **extra** delim.", TextType.TEXT)
        split_array = split_nodes_delimiter([node],DelimiterType.BOLD,TextType.BOLD)
        result_array = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("string", TextType.BOLD),
            TextNode(" value with an ", TextType.TEXT),
            TextNode("extra", TextType.BOLD),
            TextNode(" delim.", TextType.TEXT)
        ]
        self.assertEqual(split_array,result_array)

if __name__ == "__main__":
    unittest.main()
