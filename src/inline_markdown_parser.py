from textnode import TextNode, TextType
import re

def extract_markdown_images(text: str) -> list[tuple]:
    capture_img = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(capture_img, text)
    return matches
    
def extract_markdown_links(text: str) -> list[tuple]:
    capture_link = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(capture_link, text)
    return matches

def split_nodes_delimiter(
        old_nodes: list[object], delimiter: str
        ) -> list[object]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(single_node_delimiter(node, delimiter))
    
    return new_nodes


def single_node_delimiter(node: object, delimiter: str) -> list[TextNode]:
    valid_delimiters = {
        "`": TextType.CODE,
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        }
    
    if delimiter not in valid_delimiters:
        raise Exception(
            f"Invalid Delimiter. Choose from: {valid_delimiters}"
            )
    
    split_string = node.text.split(delimiter)

    #1. Check if the delimiter is unbalanced (must be an odd number of splits, meaning even number of delimiters)
    if len(split_string) % 2 == 0:
        raise ValueError(
            f"Invalid markdown: unclosed delimiter {delimiter}"
            )
    
    other_delimiters = [d for d in valid_delimiters if d != delimiter]
    target_type = valid_delimiters[delimiter]
    new_nodes = []

    for i in range(len(split_string)):
        # 2. Check for empty text, but do NOT break the index tracking loop
        if split_string[i] == "":
            continue
        
        #3. Even indexes are outside the delimiter; normal unformatted text
        if i % 2 == 0:
            new_nodes.append(TextNode(split_string[i], TextType.TEXT))

        #4. Odd indexes are inside the delimiter    
        else:
            #new_nodes.append(TextNode(split_string[i], valid_delimiters[delimiter]))
            inner_text = split_string[i]
            has_nested_delimiters = any(d in inner_text for d in other_delimiters)

            if has_nested_delimiters:
                nested_children = text_to_textnodes(inner_text)

                for child in nested_children:
                    if child.text_type == TextType.TEXT:
                        #5. Raw Text within nested delimiters, should inherit the original text_type
                        child.text_type = target_type
                    new_nodes.append(child)
            else:
                #6. Base Case: Pure text inside our delimiter, no nesting found
                new_nodes.append(TextNode(inner_text, target_type))
    return new_nodes

def split_nodes_link(old_nodes: list[object]) -> list[TextNode]:
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text
        links = extract_markdown_links(current_text)

        if not links:
            new_nodes.append(node)
            continue

        for link in links:
            alt_text, url = link

            # Split node.text in two, based on the link
            sections = current_text.split(f"[{alt_text}]({url})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

            # Inherited to check for next set of URLs, if any
            current_text = sections[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def split_nodes_images(old_nodes: list[object]) -> list[TextNode]:
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text
        links = extract_markdown_images(current_text)

        if not links:
            new_nodes.append(node)
            continue

        for link in links:
            alt_text, url = link

            # Split node.text in two, based on the link
            sections = current_text.split(f"![{alt_text}]({url})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMG, url))

            # Inherited to check for next set of URLs, if any
            current_text = sections[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[object]:
    nodes = [TextNode(text, TextType.TEXT)]

    # 1. First, split out the complex block structures (Images FIRST, then Links)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)

    # 2. Next, pass the remaining plain text blocks down the recursive engine
    nodes = split_nodes_delimiter(nodes, "**") #Bold
    nodes = split_nodes_delimiter(nodes, "_") #Italics
    nodes = split_nodes_delimiter(nodes, "`") #Code Block
    return nodes


# Test Cases-------------
# nodes = text_to_textnodes("This **is _text_** with a `code block` _word_")
# print('\n'.join([f"{node}" for node in nodes]))

# text = "This is **bold** text with an ![image](https://boot.dev) and a [link](https://boot.dev) with `code` and _italics_"

# nodes = text_to_textnodes(text)

# expected = "".join([f'{node}\n' for node in nodes])
# print(expected)