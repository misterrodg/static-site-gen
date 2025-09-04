from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def __is_heading(markdown_block: str):
    return re.search(r"^#{1,6}\s",markdown_block)

def __is_code_block(markdown_list: list[str]):
    return markdown_list[0][:3] == "```" and markdown_list[-1][-3:] == "```"

def __is_quote_block(markdown_list: list[str]):
    for line in markdown_list:
        if line[0] != ">":
            return False
    return True

def __is_ul(markdown_list: list[str]):
    for line in markdown_list:
        if line[0:2] != "- ":
            return False
    return True

def __is_ol(markdown_list: list[str]):
    for i in range(len(markdown_list)):
        if not markdown_list[i].startswith(f"{i + 1}. "):
            return False
    return True

def block_to_block_type(markdown_block: str):
    if __is_heading(markdown_block):
        return BlockType.HEADING

    markdown_list = markdown_block.split("\n")
    if __is_code_block(markdown_list):
        return BlockType.CODE
    if __is_quote_block(markdown_list):
        return BlockType.QUOTE
    if __is_ul(markdown_list):
        return BlockType.UNORDERED_LIST
    if __is_ol(markdown_list):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

