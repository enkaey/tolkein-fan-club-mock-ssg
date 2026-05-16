from parentnode import ParentNode
from leafnode import LeafNode
from inline_markdown_parser import text_to_textnodes
from textnode_to_html_node import text_node_to_html_node
from block_markdown_parser import BlockType, markdown_to_blocks, block_to_block_type

def block_to_header(block: str) -> ParentNode:
    heading_level_and_text = block.split(" ", 1)
    hash_char, clean_text = heading_level_and_text

    h_level = f"h{hash_char.count("#")}"
    children_text_nodes = text_to_textnodes(clean_text)
    children_html_nodes = [text_node_to_html_node(node) for node in children_text_nodes]
    return ParentNode(h_level, children_html_nodes)

def block_to_code(block: str) -> ParentNode:
    # Code blocks live inside preformatted tags
    code_block = block.strip("```").strip()

    return ParentNode("pre", [LeafNode("code", code_block)])

def block_to_quote(block: str) -> ParentNode:
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        if line.startswith(">"):
            clean_lines.append(line[1:].strip())
        else:
            clean_lines.append(line.strip())
    
    full_quote = " ".join(clean_lines)

    children_text_nodes = text_to_textnodes(full_quote)
    children_html_nodes = [text_node_to_html_node(node) for node in children_text_nodes]
    
    return ParentNode("blockquote", children_html_nodes)
    
def block_to_paragraph(block: str) -> ParentNode:
    children_text_nodes = text_to_textnodes(block)
    children_html_nodes = [text_node_to_html_node(node) for node in children_text_nodes]

    return ParentNode("p", children_html_nodes)

def block_to_ordered_list(block: str) -> ParentNode:
    lines = block.split("\n")

    clean_lines = [line.split(". ", 1)[1].strip() for line in lines]
    html_nodes = []

    for line in clean_lines:
        children_text_nodes = text_to_textnodes(line)
        children_html_nodes = [text_node_to_html_node(node) for node in children_text_nodes]

        html_nodes.append(ParentNode("li", children_html_nodes))
    
    return ParentNode("ol", html_nodes)

def block_to_unordered_list(block: str) -> ParentNode:
    lines = block.split("\n")

    # Identify what's been used for ul listing
    start_char = "*" if lines[0].startswith("*") else "-"

    clean_lines = [line.split(f"{start_char} ", 1)[1].strip() for line in lines]
    html_nodes = []

    for line in clean_lines:
        children_text_nodes = text_to_textnodes(line)
        children_html_nodes = [text_node_to_html_node(node) for node in children_text_nodes]

        html_nodes.append(ParentNode("li", children_html_nodes))
    
    return ParentNode("ul", html_nodes)

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    reference_block_types = {
        BlockType.HEADING: block_to_header,
        BlockType.CODE: block_to_code,
        BlockType.QUOTE: block_to_quote,
        BlockType.UNORDERED_LIST: block_to_unordered_list,
        BlockType.ORDERED_LIST: block_to_ordered_list,
        BlockType.PARAGRAPH: block_to_paragraph
    }

    child_html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # FIXED: Safe fallback defaults to paragraph if something weird slips through
        handler_func = reference_block_types.get(block_type, block_to_paragraph)
        node = handler_func(block)
        child_html_nodes.append(node)
    
    if not child_html_nodes:
        return ParentNode("div", [LeafNode(None, "")])
    
    return ParentNode("div", child_html_nodes)