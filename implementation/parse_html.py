import html2text
from nltk.tokenize import TweetTokenizer
import re


class Parser:
    def __init__(self, dbManeger):
        self.html_cleaner = html2text.HTML2Text()
        self.html_cleaner.ignore_emphasis = True
        self.html_cleaner.ignore_images = True
        self.html_cleaner.ignore_links = True
        self.html_cleaner.ignore_tables = True

        self.tknzr = TweetTokenizer()
        self.stopwords = set()

        self.tokens = []

        self.dbManager = dbManeger

    def build_stopwords(self):
        with open("data/slovenian-stopwords.txt", "r", encoding="utf-8") as stopword_file:
            stopword_file_contents = stopword_file.readlines()
        for stopword in stopword_file_contents:
            self.stopwords.add(stopword.strip())

    def get_neighbours(self, index):
        start = index - 3
        end = index + 3
        if start < 0:
            start = 0
        if end > len(self.tokens):
            end = len(self.tokens)

        neighbours = ""

        i = start
        while i < end:
            neighbours += self.tokens[i] + " "
            i += 1

        return neighbours.strip()

    def print_html(self, path):
        print("Parsing document " + path)

        # get file content
        with open(path, "r", encoding="utf-8") as content_file:
            content = content_file.read()

        # get text from html
        clean_text = self.html_cleaner.handle(content)

        # tokenize the text
        self.tokens = self.tknzr.tokenize(clean_text)

        # lower all tokens
        low_tokens = [word.lower() for word in self.tokens]

        # remove nonwords with re and stopword using a list
        # posting type:    word: [(index, neighbour), ...]
        # build a dict
        posting = {}
        for index, word in enumerate(low_tokens):
            if re.match("[a-zA-Z0-9][a-zA-Z0-9-\.]+", word) and word not in self.stopwords:
                # print(str(index) + ": " + word)
                posting.setdefault(word, [])
                posting[word].append((index, self.get_neighbours(index)))

        # insert into db
        for key, val in posting.items():
            # print(key)
            indices = str(list(map(lambda x: x[0], val))).strip("[]").replace(" ", "")
            # print(indices)
            neighbourhood = "\n".join(list(map(lambda x: x[1].strip(), val)))
            # print(neighbourhood + "\n")
            self.dbManager.insert_posting(key, path, len(val), indices, neighbourhood)

        num_words = len(posting)
        print(str(num_words) + " words in document. \n")





        # print(key, end=": ")
        #         for idx, neigh in val:
            #            insert_to_index(key, path, neigh, str(len(val)), str(list(map(lambda x: x[0], val))).strip("[ ]"))
            # str(reduce(lambda a, b: a + str(b) + ",", map(lambda x: x[0], val), ""))[:-1]
            # print("(" + str(idx) + ", " + neigh + ")", end=", ")
            # print("LEN: " + str(len(val)))
            # print(str(reduce(lambda a,b: a+str(b)+",", map(lambda x: x[0], val), ""))[:-1])

#parser = Parser()
#parser.print_html("data/evem.gov.si/evem.gov.si.1.html")



