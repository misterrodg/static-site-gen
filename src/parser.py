def markdown_to_blocks(markdown: str):
    text_blocks = markdown.split("\n\n")
    text_blocks = [item.strip() for item in text_blocks]
    return [item for item in text_blocks if item != ""]

