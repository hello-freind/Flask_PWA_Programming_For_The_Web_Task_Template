from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import database_manager as dbHandler
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        con = sqlite3.connect("database/data_source.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM actually_correct_users WHERE username=?", (username,))
        if cur.fetchone():
            error = "Username already exists. Please choose another."
        else:
            cur.execute("INSERT INTO actually_correct_users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            con.commit()
            success = "Account created successfully! You can now sign in."
        con.close()
    return render_template('/signup.html', error=error, success=success)

@app.route('/like_post', methods=['POST'])
def like_post():
    post_id = request.json.get('post_id')
    con = sqlite3.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute("UPDATE posts2 SET likes = likes + 1 WHERE post_id = ?", (post_id,))
    con.commit()
    cur.execute("SELECT likes FROM posts2 WHERE post_id = ?", (post_id,))
    likes = cur.fetchone()[0]
    con.close()
    return jsonify({'likes': likes})

@app.route('/homepage.html', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    data = dbHandler.listExtension()
    return render_template('/homepage.html', content=data)

@app.route('/add.html', methods=['GET'])
def add():
    username = session.get('username')
    con = sqlite3.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute("""
            SELECT p.id, u.username, p.post_id, p.likes, p.content, p.Title, p.timestamp
            FROM posts2 p
            LEFT JOIN actually_correct_users u ON p.id = u.id
            ORDER BY RANDOM() LIMIT 10
        """)
        random_posts = [
            {
                'id': row[0],
                'username': row[1],
                'post_id': row[2],
                'likes': row[3],
                'content': row[4],
                'Title': row[5],
                'timestamp': row[6]
            } for row in cur.fetchall()
        ]
    except Exception:
        random_posts = []
    con.close()
    return render_template('/add.html', username=username, random_posts=random_posts)

@app.route('/otherpage.html', methods=['GET'])
def otherpage():
    return render_template('/otherpage.html')

@app.route('/signin.html', methods=['GET', 'POST'])
def signin():
    error = None
    user = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        con = sqlite3.connect("database/data_source.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM actually_correct_users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        con.close()
        if user:
            session['username'] = username
            return redirect(url_for('add'))
        else:
            error = "Invalid username or password."
    return render_template('/signin.html', error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)


