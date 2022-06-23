from flask import Flask, render_template
import sqlite3

def get_db_connection():
    """
    Opens and returns a connection to the database.db file
    """
    conn = sqlite3.connect('database.db')

    # allows us to have name-based access to columns
    conn.row_factory = sqlite3.Row
    return conn



app = Flask(__name__)

@app.route('/')
def index():
    # open database connection
    conn=get_db_connection()
    # select all entries from posts table and fetch all to fetch all rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    # the posts variable is passed to the index temple 
    return render_template('index.html', posts=posts)