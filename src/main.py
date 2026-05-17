from dir_functions.copy_static import copy_static_files
from dir_functions.generate_page import generate_page, generate_pages_recursive

def main():
    copy_static_files()
    generate_pages_recursive("content/", "template.html", "public/")

if __name__ == "__main__":
    main()
