# from flask import Flask, render_template, request, redirect, url_for, session, flash

# app = Flask(__name__) 

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/members')
# def members():
#     return render_template('member.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, g
from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'asset/db/studentMember1.db'

# Fungsi untuk membuka koneksi ke database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

# Fungsi untuk menutup koneksi setelah setiap permintaan
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Fungsi untuk menjalankan kueri ke database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Fungsi untuk melakukan commit ke database
def commit_db():
    get_db().commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members', methods=['GET'])
def members():
    cursor = get_db().cursor()
    query = """
    SELECT * FROM member
    """
    cursor.execute(query)
    members = cursor.fetchall()
    cursor.close()
    return render_template('member.html', members=members)

@app.route('/contact')
def contact():
    return render_template('contact.html')


# @app.route('/quotes')
# def quotes():
#     return render_template('quotes.html')

@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
    if request.method == 'POST':
        nama = request.form['nama']
        kata = request.form['kata']

        cursor = get_db().cursor()
        query = "INSERT INTO quotes (nama, kata) VALUES (?, ?)"
        cursor.execute(query, (nama, kata))
        commit_db()
        cursor.close()

        return redirect(url_for('quotes'))

    cursor = get_db().cursor()
    query = "SELECT * FROM quotes"
    cursor.execute(query)
    quotes = cursor.fetchall()
    cursor.close()

    return render_template('quotes.html', quotes=quotes)


@app.route('/quotes/delete/<string:kata>', methods=['GET'])
def delete_quote(kata):
    cursor = get_db().cursor()
    query = "DELETE FROM quotes WHERE kata = ?"
    cursor.execute(query, (kata,))
    commit_db()
    cursor.close()
    return redirect(url_for('quotes'))

if __name__ == '__main__':
    app.run(debug=True)