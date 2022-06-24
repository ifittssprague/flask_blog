from webbrowser import get
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

# allows us to repond with a 404 page
from werkzeug.exceptions import abort



def get_db_connection():
    """
    Opens and returns a connection to the database.db file
    """
    conn = sqlite3.connect('database.db')

    # allows us to have name-based access to columns
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    """
    Gets the post with the matching post_id. Returns 404 error if no matching post exists
    """
    conn = get_db_connection()
    post = conn.execute('select * from posts where id = ?', (post_id,)).fetchone()

    conn.close()
    # if there is no matching post, a 404 error is prompted
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_hehehe'


@app.route('/')
def index():
    # open database connection
    conn=get_db_connection()
    # select all entries from posts table and fetch all to fetch all rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    # the posts variable is passed to the index temple 
    return render_template('index.html', posts=posts)


# added a variable rule that recognizes the int after the "/" in the url and passes that
# to the post function
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post = post)


@app.route('/create', methods=('GET','POST'))
def create():

    # ensures the code is only executed for a POST request
    if request.method == 'POST':
        # accessing title and content from the form data in the request object 
        title= request.form['title']
        content = request.form['content']
    
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title,content) values (?,?)', (title, content))
            conn.commit()
            conn.close()

            # after adding the post to the database, the url is redirected to the index page
            return redirect(url_for('index'))



    return render_template('create.html')

# the post we edit is determined by the url. Flask wil pass the id to the edit function
@app.route('/<int:id>/edit', methods=('GET','POST'))
def edit(id):
    post = get_post(id)

    # the new data will come in a POST request 
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        
        else:
            conn = get_db_connection()
            conn.execute('UPDATE post set title = ?, content = ? where id = ?', (title, content, id))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
    
    # in the case of a get request, we render the edit.html template and pass in the post variable
    return render_template('edit.html', post = post)
            