from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(single_node_delimiter(node, delimiter))
    
    return new_nodes


def single_node_delimiter(node, delimiter):
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


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**") #Bold
    nodes = split_nodes_delimiter(nodes, "_") #Italics
    nodes = split_nodes_delimiter(nodes, "`") #Code Block
    return nodes

# Test Cases-------------
# nodes = text_to_textnodes("This **is _text_** with a `code block` _word_")
# print('\n'.join([f"{node}" for node in nodes]))
