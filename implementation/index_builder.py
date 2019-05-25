import re
import implementation.db_manager as db_manager

words = ["test", "pretty", "much", "abc", "not", "quite"]
s1 = ["file1.html", "test 123 pretty much, test"]
s2 = ["file2.html", "abc not quite"]
docs = [s1, s2]
db_manager.recreate_index()
for word in words:
    for doc in docs:
        indexes = [m.start() for m in re.finditer(word, doc[1])]
        if len(indexes) != 0:
            db_manager.insert_posting(word, doc[0], indexes.__len__(), str(indexes).strip("[]"))
