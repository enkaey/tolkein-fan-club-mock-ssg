import os
from src.extract_title import extract_title
from src.markdown_to_html_node import markdown_to_html_node

def generate_page(
        from_path: str, template_path: str, dest_path: str, basepath: str
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

    template_v1 = template.replace("{{ Title }}", page_title)
    template_v2 = template_v1.replace("{{ Content }}", page_html)
    template_v3 = template_v2.replace('href="/', f'href="{basepath}')
    complete_template = template_v3.replace('src="/', f'src="{basepath}')

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

def generate_pages_recursive(
        from_path: str, template_path: str, dest_path: str, basepath: str
        ) -> None:
    abs_from_path = os.path.abspath(from_path)
    abs_dest_path = os.path.abspath(dest_path)

    items = os.listdir(abs_from_path)

    for item in items:
        item_path = os.path.join(abs_from_path, item)

        if os.path.isfile(item_path):
            html_filename = item.replace(".md", ".html")
            dest_item_path = os.path.join(abs_dest_path, html_filename)
            generate_page(item_path, template_path, dest_item_path, basepath)
        else:
            dest_item_path = os.path.join(abs_dest_path, item)
            generate_pages_recursive(item_path, template_path, dest_item_path, basepath)