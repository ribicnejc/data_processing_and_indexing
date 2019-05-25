import html2text

html_cleaner = html2text.HTML2Text()
html_cleaner.ignore_emphasis = True
html_cleaner.ignore_images = True
html_cleaner.ignore_links = True
html_cleaner.ignore_tables = True


def print_html(path):
    print("Hi " + path + "n")

    with open(path, "r", encoding="utf-8") as content_file:
        content = content_file.read()

    print(html_cleaner.handle(content))

print_html("data/evem.gov.si/evem.gov.si.1.html")
