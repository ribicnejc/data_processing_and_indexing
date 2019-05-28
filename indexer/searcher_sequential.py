from os import listdir
from os.path import isdir, isfile, join
from indexer.parse_html import Parser
import re
import time


parser = Parser(None)
current_milli_time = lambda: int(round(time.time() * 1000))


def search(query):
    print("Searching . . . This is gonna take a while.")

    # time it
    millis = current_milli_time()

    words = list(map(lambda x: x.lower(), query.split(" ")))
    results = []

    for word in words:
        read_files("data", results, word)

    results.sort(key=lambda x: x[1], reverse=True)

    # time it
    time_needed = current_milli_time() - millis

    # print results
    print("Results for query: \"" + query + "\"")
    print("Found results in " + str(time_needed) + " ms. \n")
    print("Displaying top 10:\n")
    print("  Frequencies".ljust(16, " ") + "|" + "  Document")
    print("".ljust(16, "-") + "|" + "".ljust(80, "-"))

    for result in results[:10]:
        print(("  " + str(result[1])).ljust(16, " ") + "|" + ("  " + result[0]).ljust(80, " "))


def read_files(path, results, word):
    for f in listdir(path):
        if isfile(join(path, f)):
            find_in_doc(join(path, f), results, word)
        else:
            read_files(join(path, f), results, word)


def find_in_doc(path, results, word):
    content = parser.get_clean_html(path)
    num = len(re.findall(word, content))
    if num > 0:
        results.append((path, num))


search("Slavko Žitnik")
