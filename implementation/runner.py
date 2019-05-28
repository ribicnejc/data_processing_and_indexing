from os import listdir
from os.path import isfile, join
from implementation.parse_html import Parser
from implementation.db_manager import dbManager

parser = Parser(dbManager)
dbManager.create_the_database()

doc_parsed = 0


def read_files(path):
    global doc_parsed
    for f in listdir(path):
        if isfile(join(path, f)):
            if f.endswith(".html"):
                parser.print_html(join(path, f))
                doc_parsed += 1
                print("Documents parsed: " + str(doc_parsed))
        else:
            read_files(join(path, f))


read_files("data")
dbManager.close_db()
