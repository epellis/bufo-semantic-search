from dataclasses import dataclass
from flask import request
from flask import Flask, render_template
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch
import re


@dataclass
class Bufo:
    path: Path
    text_name: str


ALL_THE_BUFO_DIR = Path("/Users/ned.ellis/all-the-bufo/all-the-bufo")

model = SentenceTransformer("all-MiniLM-L6-v2")

bufos = []

for filepath in ALL_THE_BUFO_DIR.iterdir():
    text_name = re.sub(r"-", " ", filepath.name)  # Replace dashes with spaces
    text_name = re.sub(r"\.\w+$", "", text_name)  # Remove the file extension
    bufos.append(Bufo(filepath, text_name))

embeddings = model.encode([b.text_name for b in bufos], convert_to_tensor=True)

app = Flask(__name__)


@app.route("/")
def index():
    query = request.args.get("query")

    if query:
        query_embedding = model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, embeddings)[0]
        top_results = torch.topk(cos_scores, k=10)

        for score, idx in zip(top_results.values, top_results.indices):
            print(bufos[idx], "(Score: {:.4f})".format(score))

    return render_template("index.html")
