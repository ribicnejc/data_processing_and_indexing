import html2text
from nltk.tokenize import TweetTokenizer
import re
from _functools import reduce
from implementation.index_builder import insert_to_index

html_cleaner = html2text.HTML2Text()
html_cleaner.ignore_emphasis = True
html_cleaner.ignore_images = True
html_cleaner.ignore_links = True
html_cleaner.ignore_tables = True

tknzr = TweetTokenizer()

# build stopword set
stopwords = set()
with open("data/slovenian-stopwords.txt", "r", encoding="utf-8") as stopword_file:
    stopword_file_contents = stopword_file.readlines()
for stopword in stopword_file_contents:
    stopwords.add(stopword.strip())


def get_neighbours(tokens, index):
    start = index - 3
    end = index + 3
    if start < 0:
        start = 0
    if end > len(tokens):
        end = len(tokens)

    neighbours = ""

    i = start
    while i < end:
        neighbours += tokens[i] + " "
        i += 1

    return neighbours.strip()


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

    # remove nonwords with re and stopword using a list
    # posting type:    word: [(index, neighbour), ...]
    # build a dict
    posting = {}
    for index, word in enumerate(low_tokens):
        if re.match("[a-zA-Z0-9][a-zA-Z0-9-\.]+", word) and word not in stopwords:
            # print(str(index) + ": " + word)
            posting.setdefault(word, [])
            posting[word].append((index, get_neighbours(low_tokens, index)))

    # insert into db
    for key, val in posting.items():
        print(key)
        indices = str(list(map(lambda x: x[0], val))).strip("[]").replace(" ", "")
        print(indices)
        neighbourhood = "\n".join(list(map(lambda x: x[1].strip(), val)))
        print(neighbourhood + "\n")

    print(len(posting))






        # print(key, end=": ")
        #         for idx, neigh in val:
            #            insert_to_index(key, path, neigh, str(len(val)), str(list(map(lambda x: x[0], val))).strip("[ ]"))
            # str(reduce(lambda a, b: a + str(b) + ",", map(lambda x: x[0], val), ""))[:-1]
            # print("(" + str(idx) + ", " + neigh + ")", end=", ")
            # print("LEN: " + str(len(val)))
            # print(str(reduce(lambda a,b: a+str(b)+",", map(lambda x: x[0], val), ""))[:-1])

print_html("data/evem.gov.si/evem.gov.si.1.html")

