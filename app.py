from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
import binascii
import os
import time

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(32)).decode('utf-8')

DATABASE = 'user_inputs.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute('CREATE TABLE IF NOT EXISTS inputs (text TEXT, timestamp INTEGER)')
        db.commit()
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def before_request():
    db = get_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text'].lower()
        db = get_db()

        timestamp = int(time.time())

        cursor = db.execute('SELECT COUNT(*) FROM inputs WHERE text = ?', (text,))
        if cursor.fetchone()[0] == 0:
            db.execute('INSERT INTO inputs (text, timestamp) VALUES (?, ?)', (text, timestamp))
            db.commit()
        else:
            flash('Bro that already exists. Why spam m9?', 'warning')

        return redirect(url_for('index'))

    cursor = get_db().execute('SELECT text, timestamp FROM inputs')
    inputs = [(row[0], row[1]) for row in cursor]

    return render_template('index.html', inputs=inputs)

if __name__ == '__main__':
    app.run(debug=True)
