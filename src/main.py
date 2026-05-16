from dir_functions.copy_static import copy_static_files
from dir_functions.generate_page import generate_page

def main():
    copy_static_files()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
