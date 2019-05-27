from os import listdir
from os.path import isdir, isfile, join
from implementation.parse_html import print_html


def read_files(path):
    for f in listdir(path):
        if isfile(join(path, f)):
            if f.endswith(".html"):
                print_html(join(path, f))
        else:
            read_files(join(path, f))


read_files("data")
