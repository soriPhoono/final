from flask import Flask, request, render_template
from sqlite3 import connect

app = Flask(__name__)

connection = connect('database.db')

with open('database/create.sql', 'r') as f:
    connection.executescript(f.read())

connection.commit()

connection.close()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form['restaurantName']
        location = request.form['location']
        cuisine = request.form['cuisine']
        dietary = request.form['dietary']
        description = request.form['description']

        connection = connect('database.db')

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO dining_options (name, location, cuisine, dietary, description) VALUES (?, ?, ?, ?, ?)",
            (name, location, cuisine, dietary, description)
        )
        connection.commit()

        connection.close()
    return render_template("submit.html")


@app.route("/favorites")
def favorites():
    return render_template("favorites.html")
