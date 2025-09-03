from enum import Enum
import re

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class DelimiterType(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
                self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode):
    text_value = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None,value=text_value)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_value)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_value)
        case TextType.CODE:
            return LeafNode(tag="code",value=text_value)
        case TextType.LINK:
            return LeafNode(tag="img",value="",props={"alt": text_value, "url": text_node.url})
        case _:
            raise Exception("Unrecognized TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if delimiter.value not in node.text:
            result.append(node)

        split_string = node.text.split(delimiter.value)

        if len(split_string) % 2 == 0:
            raise Exception("Closing delimiter not found.")

        for i in range(len(split_string)):
            node_type = text_type
            if i % 2 == 0:
                node_type = TextType.TEXT
            result.append(TextNode(split_string[i], node_type))

    return result

def extract_markdown_images(text):
    pattern = r"(?:!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

