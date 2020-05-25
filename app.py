from flask import Flask, render_template, request, redirect, session, flash, g
from cs50 import SQL
import os
app = Flask(__name__)
app.secret_key = 'somekey'

db = SQL("sqlite:///myDatabase.db")
uname = 'NU:L:L:L:L:L::::::::::::::::::::::::::::::::::::::L:::::::::::::::::::::::::L::::::::::::::'
id = -1

@app.route('/')
def langing_page():
    rows = db.execute("SELECT * FROM users")
    return render_template('Landing.html', rows=rows, uid=uname)

@app.route('/home')
def home():
    rows = db.execute("SELECT * FROM posts")
    people = db.execute("SELECT * FROM users")
    return render_template('Home.html', rows=rows, people=people)

@app.route('/home/<subPage>')
def homeSubPage(subPage):
    link = int(subPage)
    status_rows = db.execute("SELECT id FROM posts WHERE id IS :subPage", subPage=link)
    stat = False
    for i in status_rows:
        if i["id"] == int(subPage):
            stat = True
    if stat:
        return render_template("subPost.html", subPage=subPage, row = db.execute("SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id IS :id", id=link))
    else:
        return "404 error this is not a valid page"

@app.route('/postIt', methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template('postIt.html')
    elif request.method == "POST":
        # get the id of the user
        uid = id
        # if the id is -1 redirect to the login page
        if (id == -1):
            return redirect('/login')
        # add to the posts table the description and the title (image do last or sometime else)
        title = request.form.get("title")
        description = request.form.get("description")
        db.execute("INSERT INTO posts (user_id, title, description) VALUES (:uid, :title, :description)", uid=uid, title=title, description=description)
        return redirect('/home')

@app.route('/login', methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    rows = db.execute("SELECT userName, userPassword, id FROM users WHERE userName IS :username AND userPassword IS :password", username=username, password=password)
    if request.method == "POST" and len(rows) == 1:
        session.pop('user_id', None)
        global uname 
        global id
        uname = rows[0]["userName"]
        id = rows[0]["id"]
        session['user_id'] = id
        return redirect('/')
    else:
        return render_template('Login.html', status=1)

@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("Signup.html")
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT userName FROM users WHERE userName IS :name", name=name)
        if (len(rows) == 0):
            db.execute("INSERT INTO users (userName, userPassword) VALUES(:name, :password)", name=name, password=password)
        else:
            print('The user name was already a thing')
        return redirect('/')
        

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()