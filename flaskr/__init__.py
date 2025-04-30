from sqlite3 import connect
from flask import Flask, request, render_template, redirect

DATABASE_PATH = "./database/"
PRIMARY_DATABASE = f"{DATABASE_PATH}database.db"

app = Flask(__name__)

connection = connect(PRIMARY_DATABASE)

with open(f'{DATABASE_PATH}create.sql', 'r') as f:
    connection.executescript(f.read())

connection.commit()

connection.close()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        
        connection = connect(PRIMARY_DATABASE)
        cursor = connection.cursor()
        query = """
            SELECT name, location, cuisine, dietary, description 
            FROM dining_options 
            WHERE name LIKE ? OR location LIKE ? OR cuisine LIKE ? OR dietary LIKE ?
        """
        keyword_wildcard = f"%{keyword}%"
        cursor.execute(query, (keyword_wildcard, keyword_wildcard, keyword_wildcard, keyword_wildcard))
        results = cursor.fetchall()
        connection.close()

    return render_template("search.html", results=results)



@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form['restaurantName']
        location = request.form['location']
        cuisine = request.form['cuisine']
        dietary = request.form['dietary']
        description = request.form['description']

        connection = connect(PRIMARY_DATABASE)

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO dining_options (name, location, cuisine, dietary, description) VALUES (?, ?, ?, ?, ?)",
            (name, location, cuisine, dietary, description)
        )
        connection.commit()

        connection.close()

        return redirect("/submit/confirm")
    elif request.method == "GET":
        return render_template("submit.html")


@app.route("/submit/confirm")
def submit_confirm():
    return render_template("submit-confirm.html")


@app.route("/favorites")
def favorites():
    return render_template("favorites.html")
