from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/')
def regist():
    return render_template('regist.html')

if __name__ == "__main__":
    app.run(debug=True)
"""
def profile():
    return render_template("profil.html")
"""
