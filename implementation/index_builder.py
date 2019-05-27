import re
import implementation.db_manager as db_manager

words = ["test", "pretty", "much", "abc", "not", "quite"]
s1 = ["file1.html", "test 123 pretty much, test"]
s2 = ["file2.html", "abc not quite"]
docs = [s1, s2]


def clear_database():
    db_manager.recreate_index()


def insert_to_index(word, path, neighbor_text, frequency, indexes):
    db_manager.insert_posting(word, path, frequency, indexes, neighbor_text)


clear_database()
insert_to_index("song", "test.html", "singing a song with someone", 3, "[1, 2, 3]")
