from os import listdir
from os.path import isdir, isfile, join
from implementation.parse_html import Parser
from implementation.index_builder import clear_database
from implementation.db_manager import dbManager

parser = Parser(dbManager)

def read_files(path):
    for f in listdir(path):
        if isfile(join(path, f)):
            if f.endswith(".html"):
                parser.print_html(join(path, f))
        else:
            read_files(join(path, f))


read_files("data")
dbManager.close_db()
