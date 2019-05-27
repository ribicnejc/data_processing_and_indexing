import sqlite3

conn = sqlite3.connect('inverted-index.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IndexWord (
        word TEXT PRIMARY KEY
    );
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

c.execute('''create table Neighbors
 (
   word text not null,
   documentName text not null,
   indexPosition text not null,
   neighborText text,
   primary key(word, documentName, indexPosition),
   foreign key (word, documentName) references Posting(word, documentName)
 ); ''')

# Save (commit) the changes
conn.commit()
conn.close()
