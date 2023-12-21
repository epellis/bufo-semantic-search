from dataclasses import dataclass
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer, util
import torch

ALL_THE_BUFO_DIR = Path("/Users/ned.ellis/all-the-bufo/all-the-bufo")


@dataclass
class Bufo:
    path: Path
    text_name: str


def _filename_to_search_name(filepath: Path):
    text_name = re.sub(r"-", " ", filepath.name)  # Replace dashes with spaces
    text_name = re.sub(r"\.\w+$", "", text_name)  # Remove the file extension
    return text_name


class BufoSearchIndex:
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.bufos = [
            Bufo(path=fp, text_name=_filename_to_search_name(fp))
            for fp in ALL_THE_BUFO_DIR.iterdir()
        ]

        self.embeddings = self.model.encode(
            [b.text_name for b in self.bufos], convert_to_tensor=True
        )

    def search(self, query: str) -> list[tuple[float, Bufo]]:
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=10)

        bufos = [self.bufos[i] for i in top_results.indices]
        return list(zip(top_results.values, bufos))
