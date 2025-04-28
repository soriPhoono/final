from flask import Flask, request, url_for, render_template, redirect
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


@app.post('/handle_add')
def handle_add():
    if request.method == "POST":
        name = request.form.get("restaurantName")
        location = request.form.get("location")
        cuisine = request.form.get("cuisine")
        dietary = request.form.get("dietary")
        description = request.form.get("description")

        print(name, location, cuisine, dietary, description)

        connection = connect('database.db')

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO dining_options (name, location, cuisine, dietary, description) VALUES (?, ?, ?, ?, ?)",
            (name, location, cuisine, dietary, description))
        connection.commit()

        connection.close()
    return render_template("search.html")

@app.route("/favorites")
def favorites():
    return render_template("favorites.html")
