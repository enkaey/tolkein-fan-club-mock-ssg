from dir_functions.copy_static import copy_static_files
from dir_functions.generate_page import generate_pages_recursive
import sys


def main():
    copy_static_files("static", "docs")

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive("content/", "template.html", "docs/", basepath)
    

if __name__ == "__main__":
    main()
