import sqlite3


def insert_posting(word, doc_path, f, indexes):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    if not word_exists(word):
        insert_word(word)
    if doc_exists(doc_path, word):
        return
    query = '''
        INSERT INTO Posting (word, documentName, frequency, indexes) VALUES
            ('{}', '{}', {}, '{}');
    '''.format(word, doc_path, f, indexes)
    c.execute(query)
    conn.commit()
    conn.close()


def insert_word(word):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    query = '''
            INSERT INTO IndexWord (word) VALUES
                ('{}');
        '''.format(word)
    c.execute(query)
    conn.commit()
    conn.close()


def word_exists(word):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    query = '''
                SELECT * FROM IndexWord WHERE word = '{}';
            '''.format(word)
    cursor = c.execute(query)
    empty = cursor.fetchall().__len__() != 0
    conn.close()
    return empty


def doc_exists(doc, word):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    query = '''
                    SELECT * FROM Posting WHERE documentName = '{}' AND word = '{}';
                '''.format(doc, word)
    cursor = c.execute(query)
    empty = cursor.fetchall().__len__() != 0
    conn.close()
    return empty


def recreate_index():
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    c.execute('''
            DROP TABLE IndexWord
        ''')
    c.execute('''
        CREATE TABLE IndexWord (
            word TEXT PRIMARY KEY
        );
    ''')
    c.execute('''
            DROP TABLE Posting
        ''')
    c.execute('''
        CREATE TABLE Posting (
            word TEXT NOT NULL,
            documentName TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            indexes TEXT NOT NULL,
            PRIMARY KEY(word, documentName),
            FOREIGN KEY (word) REFERENCES IndexWord(word)
        );
    ''')
    conn.close()
