import sqlite3

# connection is create to a database file named database.db
connection = sqlite3.connect('database.db')

# the schema.sql file is opened and all sql statements in it are executed 
with open('schema.sql') as f:
    connection.executescript(f.read())

# cursor object is created and then two 
cur = connection.cursor()

cur.execute(" INSERT INTO POSTS (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute(" INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )


connection.commit()
connection.close()

