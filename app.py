from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import random
import string

hostlink = "127.0.0.1:5000/"

app = Flask(__name__)
db = SQLAlchemy(app)


def getselectdata(link):
    sqlconnection = sqlite3.connect("F:\\14 v 2.0\\urls.db")
    cursor = sqlconnection.cursor()
    data = cursor.execute('SELECT * FROM links where redirect_url="' + str(link) + '"')
    return data


def insertdata(query):
    sqlconnection = sqlite3.connect("F:\\14 v 2.0\\urls.db")
    cursor = sqlconnection.cursor()
    cursor.execute(query)
    sqlconnection.commit()
    sqlconnection.close()


def generate_random_string(length):
    letters = string.ascii_lowercase
    stringname = ''.join(random.choice(letters) for i in range(length))
    return stringname


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        global link
        link = request.form['link']

        linkname = generate_random_string(8)

        insertdata("INSERT INTO links VALUES ('" + link + "','" + hostlink + linkname + "')")

        return redirect(url_for('shorturl', link=linkname))

    if request.method == 'GET':
        return render_template("index.html")



@app.route('/<link>')
def getlink(link):
    data = getselectdata(hostlink + link)
    link = list(data)[0][0]

    if (link == "http://127.0.0.1:5000/<link>"):
        return redirect(link)
    else:
        return redirect("http://" + link)


@app.route('/shorturl/<link>', methods=['GET', 'POST'])
def shorturl(link):
    if request.method == 'POST':
        aredirect = request.form['redirect']
        if request.form['redirect'] == 'Перейти':
            return redirect('/' + link)
        if request.form['redirect'] == 'Изменить ссылку':
            return redirect(url_for('changedlink'))
    if request.method == 'GET':
        data = getselectdata(hostlink + link)
        return render_template("shorturl.html", created_link=list(data)[0][1])


@app.route('/changedlink', methods=['GET', 'POST'])
def changedlink():
    if request.method == 'POST':
        namelink = request.form['changed']
        insertdata("INSERT INTO links VALUES ('" + link + "','" + hostlink + namelink + "')")
        return redirect(url_for('shorturl', link=namelink))
    if request.method == 'GET':
        return render_template("changedlink.html")

@app.route('/listik')
def listik():
    sqlconnection = sqlite3.connect("F:\\14 v 2.0\\urls.db")
    cur = sqlconnection.cursor()
    cur.execute("SELECT * FROM links")
    items = cur.fetchall()
    return render_template('list.html', items=items)


if __name__ == "__main__":
    app.run(debug=True)
