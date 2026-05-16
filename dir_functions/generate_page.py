import os
from src.extract_title import extract_title
from src.markdown_to_html_node import markdown_to_html_node

def generate_page(
        from_path: str, template_path: str, dest_path: str
        ) -> None:
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    abs_from_path = os.path.abspath(from_path)
    abs_template_path = os.path.abspath(template_path)
    abs_dest_path = os.path.abspath(dest_path)

    with open(abs_from_path, "r") as file:
        markdown = file.read()
    
    with open(abs_template_path, "r") as file:
        template = file.read()
    
    html_node = markdown_to_html_node(markdown)
    page_html =  html_node.to_html()
    page_title = extract_title(markdown)

    template_with_title = template.replace("{{ Title }}", page_title)
    complete_template = template_with_title.replace("{{ Content }}", page_html)

    #Create the file

    # 1. Check if the destination path is a folder or an explicit file
    # splitext splits "public/index.html" into ("public/index", ".html")
    _, extension = os.path.splitext(abs_dest_path)

    if extension == "":
        # If there's no file extension, the user gave us a directory folder!
        # Automatically append "index.html" to the path
        abs_dest_path = os.path.join(abs_dest_path, "index.html")

    dest_dir = os.path.dirname(abs_dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(abs_dest_path, "w") as file:
        file.write(complete_template)