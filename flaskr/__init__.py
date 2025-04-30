from urllib.parse import quote_plus
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


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    cuisine = request.args.get('cuisine', '')
    dietary = request.args.get('dietary', '')

    connection = connect(PRIMARY_DATABASE)
    cursor = connection.cursor()

    sql = "SELECT * FROM dining_options WHERE (LOWER(name) LIKE ? OR LOWER(location) LIKE ?)"
    params = [f"%{query.lower()}%", f"%{query.lower()}%"]

    if cuisine:
        sql += " AND LOWER(cuisine) = ?"
        params.append(cuisine.lower())

    if dietary:
        sql += " AND LOWER(dietary) = ?"
        params.append(dietary.lower())

    cursor.execute(sql, params)
    search_results = cursor.fetchall()
    connection.close()

    connection = connect(PRIMARY_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dining_options")
    all_restaurants = cursor.fetchall()
    connection.close()

    return render_template("search.html", search_results=search_results, all_restaurants=all_restaurants, query=query, cuisine=cuisine, dietary=dietary)


@app.route("/delete/<int:restaurant_id>", methods=["POST"])
def delete_restaurant(restaurant_id):
    connection = connect(PRIMARY_DATABASE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM dining_options WHERE id = ?", (restaurant_id,))
    connection.commit()
    connection.close()

    return redirect("/search")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form['restaurantName']
        raw_location = request.form['location']
        cuisine = request.form['cuisine']
        dietary = request.form['dietary']
        description = request.form['description']

        encoded_location = quote_plus(raw_location)
        maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_location}"

        connection = connect(PRIMARY_DATABASE)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO dining_options (name, location, cuisine, dietary, description) VALUES (?, ?, ?, ?, ?)",
            (name, maps_link, cuisine, dietary, description)
        )
        connection.commit()
        connection.close()

        return redirect("/submit/confirm")
    elif request.method == "GET":
        return render_template("submit.html")


@app.route("/submit/confirm")
def submit_confirm():
    return render_template("submit-confirm.html")
