from dataclasses import dataclass
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer, util
import torch

ALL_THE_BUFO_DIR = Path("/Users/ned.ellis/all-the-bufo/all-the-bufo")


@dataclass
class ScoredBufo:
    path: Path
    score: float


def _filename_to_search_name(filepath: Path):
    text_name = re.sub(r"-", " ", filepath.name)  # Replace dashes with spaces
    text_name = re.sub(r"\.\w+$", "", text_name)  # Remove the file extension
    return text_name


class BufoSearchIndex:
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.bufos = list(ALL_THE_BUFO_DIR.iterdir())

        bufo_text_names = [_filename_to_search_name(fp) for fp in self.bufos]
        self.embeddings = self.model.encode(bufo_text_names, convert_to_tensor=True)

    def search(self, query: str) -> list[ScoredBufo]:
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=10)

        results = []
        for idx, score in zip(top_results.indices, top_results.values):
            results.append(ScoredBufo(path=self.bufos[idx], score=score))

        return results
