from flask import Flask, request, url_for, render_template, redirect
from sqlite3 import connect

app = Flask(__name__)

connection = connect('database.db')


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
