import html2text
from nltk.tokenize import TweetTokenizer

html_cleaner = html2text.HTML2Text()
html_cleaner.ignore_emphasis = True
html_cleaner.ignore_images = True
html_cleaner.ignore_links = True
html_cleaner.ignore_tables = True


tknzr = TweetTokenizer()


def print_html(path):
    # get file content
    with open(path, "r", encoding="utf-8") as content_file:
        content = content_file.read()

    # get text from html
    clean_text = html_cleaner.handle(content)

    # tokenize the text
    tokens = tknzr.tokenize(clean_text)

    # lower all tokens
    low_tokens = [word.lower() for word in tokens]

    # print lowered tokens
    for word in low_tokens:
        print(word)


print_html("data/evem.gov.si/evem.gov.si.1.html")
