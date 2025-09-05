from blocknode import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnode

import re

def extract_title(markdown: str) -> str:
    level, result = __clean_heading([markdown])
    if level != 1:
        raise Exception("h1 not found")
    return result

def markdown_to_blocks(markdown: str):
    text_blocks = markdown.split("\n\n")
    text_blocks = [item.strip() for item in text_blocks]
    return [item for item in text_blocks if item != ""]

def __clean_paragraph(block: list[str]) -> str:
    return " ".join(block)

def __clean_heading(block: list[str]) -> tuple[int, str]:
    full_header = block[0]
    text = full_header.lstrip("#")
    level = len(full_header) - len(text)
    text = text.strip()
    return (level, text)

def __clean_quote(block: list[str]) -> str:
    result = ""
    for line in block:
        result += line.lstrip("> ")
    return result

def __split_unordered_items(block: list[str]) -> list[str]:
    result = []
    for line in block:
        result.append(line.lstrip("- "))
    return result

def __split_ordered_items(block: list[str]) -> list[str]:
    result = []
    for line in block:
        match = re.match(r"(?:\d*\.\s)(.*)",line)
        if match:
            result.append(match.group(1))
    return result

def __clean_code(block: list[str]) -> str:
    return "\n".join([line.strip("```") for line in block if line.strip("```") != ""])

def __text_to_children(block: list[str]) -> list[HTMLNode]:
    result = []
    for line in block:
        text_nodes = text_to_textnode(line)
        for node in text_nodes:
            result.append(text_node_to_html_node(node))
    return result

def __process_heading(block: list[str]) -> ParentNode:
    level, text = __clean_heading(block)
    children = __text_to_children([text])
    return ParentNode(f"h{level}",children)

def __process_quote(block: list[str]) -> ParentNode:
    text = __clean_quote(block)
    children = __text_to_children([text])
    return ParentNode("blockquote",children)

def __process_ul(block: list[str]) -> ParentNode:
    text_list = __split_unordered_items(block)
    children = __text_to_children(text_list)
    for child in children:
        child.value = f"<li>{child.value}</li>"
    return ParentNode("ul",children)

def __process_ol(block: list[str]) -> ParentNode:
    text_list = __split_ordered_items(block)
    children = __text_to_children(text_list)
    for child in children:
        child.value = f"<li>{child.value}</li>"
    return ParentNode("ol",children)

def __process_code(block: list[str]) -> ParentNode:
    text = __clean_code(block)
    children = [LeafNode("code",text)]
    return ParentNode("pre",children)

def __process_paragraph(block: list[str]) -> ParentNode:
    text = __clean_paragraph(block)
    children = __text_to_children([text])
    return ParentNode("p",children)

def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_list = block.split("\n")
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(__process_paragraph(block_list))
            case BlockType.HEADING:
                children.append(__process_heading(block_list))
            case BlockType.CODE:
                children.append(__process_code(block_list))
            case BlockType.QUOTE:
                children.append(__process_quote(block_list))
            case BlockType.UNORDERED_LIST:
                children.append(__process_ul(block_list))
            case BlockType.ORDERED_LIST:
                children.append(__process_ol(block_list))

    return ParentNode("div",children)
