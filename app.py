from pathlib import Path
from flask import request
from flask import Flask, render_template
from bufo.search_index import BufoSearchIndex


app = Flask(__name__)

searcher = BufoSearchIndex()


@app.route("/")
def index():
    query = request.args.get("query")

    results = None
    if query:
        results = searcher.search(query)

    print(results)

    return render_template("index.html", results=results)
