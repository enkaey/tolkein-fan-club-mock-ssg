from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def validate_ordered_list(block: str) -> bool:
    lines = block.split("\n")
    return all(
        [line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)]
        )

def validate_unordered_list(block: str) -> bool:
    lines = block.split("\n")
    return all(
        line.startswith("- ") or line.startswith("* ") for line in lines
        )

def validate_quote_block(block: str) -> bool:
    lines = block.split("\n")
    return all(
        line.startswith(">") for line in lines
    )

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.strip().split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]

def block_to_block_type(block: str) -> Enum:
    if block.startswith(
        ("# ", "## ", "### ", "#### ", "##### ", "###### ")
        ):
        return BlockType.HEADING
    
    elif len(block) >= 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    elif validate_quote_block(block):
        return BlockType.QUOTE
    
    elif validate_unordered_list(block):
        return BlockType.UNORDERED_LIST
    
    elif validate_ordered_list(block):
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH