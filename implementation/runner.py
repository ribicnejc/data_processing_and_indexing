from os import listdir
from os.path import isdir, isfile, join
from implementation.parse_html import print_html
from implementation.index_builder import clear_database


clear_database()


def read_files(path):
    for f in listdir(path):
        if isfile(join(path, f)):
            if f.endswith(".html"):
                print("Parsing file: " + f)
                print_html(join(path, f))
        else:
            read_files(join(path, f))


read_files("data")
