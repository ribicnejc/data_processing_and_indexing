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

    def word_exists(self, word):
        query = "SELECT * FROM IndexWord WHERE word = ?;"
        cursor = self.cur.execute(query, (word,))
        empty = cursor.fetchall().__len__() != 0
        return empty

    def insert_word(self, word):
        query = "INSERT INTO IndexWord (word) VALUES (?);"
        self.cur.execute(query, (word,))
        #self.conn.commit()

    def insert_posting(self, word, doc_path, freq, indexes, neighbor_text):
        if not self.word_exists(word):
            self.insert_word(word)
        query = "INSERT INTO Posting (word, documentName, frequency, indexes, neighbourhood) VALUES(?, ?, ?, ?, ?);"
        self.cur.execute(query, (word, doc_path, freq, indexes, neighbor_text))
        #self.conn.commit()

    def close_db(self):
        self.conn.commit()
        self.conn.close()


dbManager = DBManager()

