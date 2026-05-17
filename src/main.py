from dir_functions.copy_static import copy_static_files
from dir_functions.generate_page import generate_page, generate_pages_recursive

def main():
    copy_static_files()

    # Home Page
    generate_page("content/index.md", "template.html", "public/index.html")

    # Blog Pages
    generate_pages_recursive("content/", "template.html", "public/")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")

    # Contact Page
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")


if __name__ == "__main__":
    main()
