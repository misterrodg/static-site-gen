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
    def __init__(
            self,
            text: str,
            text_type: TextType,
            url: str | None = None
    ):
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

def split_nodes_delimiter(
        old_nodes: list,
        delimiter: DelimiterType,
        text_type: TextType
):
    for i in range(len(old_nodes)):
        if delimiter.value not in old_nodes[i].text:
            continue

        split_string = old_nodes[i].text.split(delimiter.value)

        if len(split_string) % 2 == 0:
            raise Exception("Closing delimiter not found.")

        new_items = []
        for j in range(len(split_string)):
            node_type = text_type
            if j % 2 == 0:
                node_type = TextType.TEXT
            new_items.append(TextNode(split_string[j], node_type))
        old_nodes[i:i+1] = new_items
    return old_nodes

def extract_markdown_images(text: str):
    pattern = r"(?:!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str):
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def __handle_sections(
    node: TextNode,
    links: list[tuple[str,str]],
    is_image: bool = False
):
    result = []
    lead_char = ""
    text_type = TextType.LINK
    remaining_text = node.text

    if is_image:
        lead_char = "!"
        text_type = TextType.IMAGE

    for i in range(len(links)):
        link_text, link_url = links[i]
        sections = remaining_text.split(f"{lead_char}[{link_text}]({link_url})",1)
        for j in range(len(sections)):
            if j % 2 != 0:
                result.append(TextNode(link_text, text_type, link_url))
                continue
            result.append(TextNode(sections[j], TextType.TEXT))
        remaining_text = sections[-1]
    if remaining_text != "":
        result.append(TextNode(remaining_text, TextType.TEXT))
    return result

def split_nodes_image(old_nodes: list[TextNode]):
    for i in range(len(old_nodes)):
        image_links = extract_markdown_images(old_nodes[i].text)
        if len(image_links) == 0:
            continue

        new_nodes = __handle_sections(old_nodes[i], image_links, True)
        old_nodes[i:i+1] = new_nodes
    return old_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    for i in range(len(old_nodes)):
        links = extract_markdown_links(old_nodes[i].text)
        if len(links) == 0:
            continue

        new_nodes = __handle_sections(old_nodes[i], links)
        old_nodes[i:i+1] = new_nodes
    return old_nodes

