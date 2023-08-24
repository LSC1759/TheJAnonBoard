from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
import binascii
import os
import nltk
from nltk.corpus import words as nltk_words #for dictionary checking

nltk.download('words')

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(32)).decode('utf-8')

DATABASE = 'user_inputs.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:                #added so that when u run you dont have to make db urself
        db = g._database = sqlite3.connect(DATABASE)
        db.execute('CREATE TABLE IF NOT EXISTS inputs (text TEXT)')
        db.commit()
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request #so why is this here idk u tell me
def before_request():
    db = get_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text'].lower()
        db = get_db()

        words_in_text = text.split()  # splitting sentences yolo
        are_all_words_english = all(word in nltk_words.words() for word in words_in_text)

        if not are_all_words_english:  # check for eng words
            flash('ENGLISH words only :pray:  suggest other idea for filtering idk', 'warning')
        else:
            cursor = db.execute('SELECT COUNT(*) FROM inputs WHERE text = ?', (text,))
            if cursor.fetchone()[0] == 0:
                db.execute('INSERT INTO inputs (text) VALUES (?)', (text,))
                db.commit()
            else:
                flash('Bro that already exists. Why spam m9?', 'warning')

        # after done return to page so that user doesnt go crazy about why his text isnt there cuz he didnt refresh xd (auto refresh basically)
        return redirect(url_for('index'))

    cursor = get_db().execute('SELECT text FROM inputs')
    inputs = [row[0] for row in cursor]

    return render_template('index.html', inputs=inputs)

if __name__ == '__main__':
    app.run(debug=True)
