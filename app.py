from flask import request
from flask import Flask, render_template
from search_index import BufoSearchIndex


app = Flask(__name__)

searcher = BufoSearchIndex()


@app.route("/")
def index():
    query = request.args.get("query")

    if query:
        results = searcher.search(query)
        print(results)

    return render_template("index.html")
