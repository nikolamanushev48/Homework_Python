import uuid
import os
from flask import Flask,render_template,request,redirect, url_for,make_response
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import Column, Integer, String, ForeignKey
from database import init_db,db_session,Base
from login import login_manager
from models import User,Topic,Post
from utils import validate_file_type, split_in_groups, generate_room_id


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
login_manager.init_app(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "nikola"
db = SQLAlchemy(app)
init_db()

@app.teardown_appcontext
def shutdown_context(exception=None):
    db_session.remove()
"""
class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(String(80), unique=True,nullable="False")
    password = db.Column(String(120), unique=True,nullable="False")
    def __repr__(self):
        return '<User %r>' % self.username
"""

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db_session.add(user)
        db_session.commit()
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = None
    if request.method == 'GET':
        response = make_response(render_template('login.html',user = current_user))
    else:
        response = make_response(redirect(url_for('mainPage')))

        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            user.login_id = str(uuid.uuid4())
            db_session.commit()
            login_user(user)
    return response



@app.route("/logout")
@login_required
def logout():
    current_user.login_id = None
    db_session.commit()
    logout_user()
    return redirect(url_for('login'))

@app.route("/topic",methods = ['GET','POST'])
def topic():
    if request.method == 'GET':
        return render_template("topic.html")
    else:
        title = request.form['Title']
        description = request.form['description']
        topic = Topic(name= title,description = description)
        db_session.add(topic)
        db_session.commit()
    return redirect(url_for('mainPage'))

@app.route('/', methods = ['GET'])
def mainPage():
    topics = Topic.query.all()

    return render_template("mainpage.html",user=current_user,topics = topics)
    #return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
