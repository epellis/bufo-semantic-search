from flask import request
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    print(request.args.get("query"))
    return render_template("index.html")
