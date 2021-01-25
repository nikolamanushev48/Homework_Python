from flask import Flask,render_template,request,redirect, url_for,make_response
from flask_sqlalchemy import SQLAlchemy
#from flask_socketio import SocketIO, join_room, send
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True,nullable="False")
    password = db.Column(db.String(120), unique=True,nullable="False")
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        User(username = username ,password = password)
    return render_template("register.html")


@app.route('/login',methods = ["POST", "GET"])
def login():
    if request == "POST":
        if request.form == User.username:
            return "AAAAAAA"
    return render_template("login.html")


@app.route('/')
def mainPage():
    return render_template("mainpage.html")

if __name__ == "__main__":
    app.run(debug=True)


"""
app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"
    #return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
"""

