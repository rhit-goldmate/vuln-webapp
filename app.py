from flask import Flask, request, redirect, render_template, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # weak secret key on purpose

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute('INSERT INTO users (username, password) VALUES ("admin", "password")')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Vulnerable to SQL Injection!
        c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        result = c.fetchone()
        conn.close()
        if result:
            session['user'] = username
            return redirect(url_for('upload'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        # No file type checking -- vulnerable to Unrestricted File Upload
        file.save(os.path.join('uploads', file.filename))
        return "File uploaded successfully!"
    return render_template('upload.html')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        comment = request.form['comment']
        # Reflecting input without sanitization -- vulnerable to XSS
        return f"You said: {comment}"
    return render_template('comment.html')

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
