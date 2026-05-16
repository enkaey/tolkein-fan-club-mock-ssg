from block_markdown_parser import markdown_to_blocks

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    h1 = [
        block.lstrip("# ") for block in blocks if block.startswith("# ")][0]
    return h1