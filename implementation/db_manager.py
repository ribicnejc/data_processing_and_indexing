import sqlite3


class DBManager:
    def __init__(self):
        self.conn = conn = sqlite3.connect('inverted-index.db')
        self.cur = conn.cursor()

        self.create_the_database()

    def create_the_database(self):
        self.cur.execute('''	
            DROP TABLE IF EXISTS IndexWord;
        ''')

        self.cur.execute('''
            DROP TABLE IF EXISTS Posting;
        ''')

        self.cur.execute('''	
            CREATE TABLE IndexWord (
                word TEXT PRIMARY KEY
            );
        ''')

        self.cur.execute('''	   
            CREATE TABLE Posting (
                word TEXT NOT NULL,
                documentName TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                indexes TEXT NOT NULL,
                neighbourhood TEXT NOT NULL,
                PRIMARY KEY(word, documentName)
                FOREIGN KEY (word) REFERENCES IndexWord(word)
            );
            ''')

        self.conn.commit()
        self.conn.close()

        def word_exists(self, word):
            query = '''
                        SELECT * FROM IndexWord WHERE word = '{}';
                    '''.format(word)
            cursor = self.cur.execute(query)
            empty = cursor.fetchall().__len__() != 0
            return empty

        def insert_word(self, word):
            query = '''
                    INSERT INTO IndexWord (word) VALUES
                        ('{}');
                '''.format(word)
            self.cur.execute(query)
            self.conn.commit()

        def insert_posting(self, word, doc_path, freq, indexes, neighbor_text):
            if not word_exists(word):
                self.insert_word(word)
            query = '''
                INSERT INTO Posting (word, documentName, frequency, indexes, neighbourhood) VALUES
                    ('{}', '{}', {}, '{}', '{}');
            '''.format(word, doc_path, freq, indexes, neighbor_text)
            self.cur.execute(query)
            self.conn.commit()


dbManager = DBManager()


def insert_posting(word, doc_path, f, indexes, neighbor_text):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    if not word_exists(word):
        insert_word(word)
    if not neighbor_exists(word, doc_path, indexes):
        insert_neighbor(word, doc_path, indexes, neighbor_text)
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


def insert_neighbor(word, path, index_position, text):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    query = '''
            INSERT INTO Neighbors (word, documentName, indexPosition, neighborText) VALUES
                ('{}', '{}', '{}', '{}');
        '''.format(word, path, index_position, text)
    c.execute(query)
    conn.commit()
    conn.close()


def neighbor_exists(word, path, index_position):
    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()
    query = '''
                SELECT * FROM Neighbors WHERE word = '{}' and documentName = '{}' and indexPosition = '{}';
            '''.format(word, path, index_position)
    cursor = c.execute(query)
    empty = cursor.fetchall().__len__() != 0
    conn.close()
    return empty


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
    # c.execute('''
    #         DROP TABLE IF IndexWord
    #     ''')
    c.execute('''
        CREATE TABLE IndexWord (
            word TEXT PRIMARY KEY
        );
    ''')
    # c.execute('''
    #         DROP TABLE Posting
    #     ''')
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
    # c.execute('''
    #         DROP TABLE Neighbors
    #     ''')
    c.execute('''create table Neighbors
     (
       word text not null,
       documentName text not null,
       indexPosition text not null,
       neighborText text,
       primary key(word, documentName, indexPosition),
       foreign key (word, documentName) references Posting(word, documentName)
     ); ''')
    conn.close()



