from flask import request
from flask import Flask, render_template, send_from_directory
from bufo.search_index import BufoSearchIndex, ALL_THE_BUFO_DIR


app = Flask(__name__)

searcher = BufoSearchIndex()


@app.route("/")
def index():
    query = request.args.get("query")

    results = None
    if query:
        results = searcher.search(query)

    return render_template("index.html", results=results)


@app.route("/assets/<filename>")
def get_asset(filename: str):
    return send_from_directory(ALL_THE_BUFO_DIR, filename)
