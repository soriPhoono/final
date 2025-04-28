from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        print("test")

        return render_template("index.html")
    elif request.method == 'GET':
        return render_template("index.html")
