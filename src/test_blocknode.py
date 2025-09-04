import unittest

from blocknode import BlockType, block_to_block_type

class TestBlockNode(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        md = "# Heading 1"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

        md = "## Heading 2"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

        md = "### Heading 3"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

        md = "#### Heading 4"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

        md = "##### Heading 5"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

        md = "###### Heading 6"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)


        md = "####### Heading 7"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md = "```\nThis is a code block.\nWith multiple lines of text.\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = "> Quotes in markdown\n> are often helpful.\n> - Abraham Lincoln"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)


    def test_block_to_block_type_ul(self):
        md = "- Item A\n- Item B\n- Item C"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)


    def test_block_to_block_type_ol(self):
        md = "1. Item 1\n2. Item 2\n3. Item 3"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

        md = "1. Item A\n2. Item B\n13. Item C"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_para(self):
        md = "```\n> \n- \n1. "
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

