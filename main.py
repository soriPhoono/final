from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")

@app.route('/api/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comments = request.form['comments']

        print(name, email, comments)
