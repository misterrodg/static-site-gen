import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "Header1")
        self.assertEqual(str(node), "h1 Header1")

if __name__ == "__main__":
    unittest.main()
