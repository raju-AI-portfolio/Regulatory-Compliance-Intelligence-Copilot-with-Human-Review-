import os
import json
import faiss
from sentence_transformers import SentenceTransformer

from app.config import INDEX_FOLDER, EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def load_regulation_store(regulation: str):
    reg_folder = os.path.join(INDEX_FOLDER, regulation.lower())

    index = faiss.read_index(os.path.join(reg_folder, "index.faiss"))

    with open(os.path.join(reg_folder, "texts.json"), "r", encoding="utf-8") as f:
        texts = json.load(f)

    with open(os.path.join(reg_folder, "metadatas.json"), "r", encoding="utf-8") as f:
        metadatas = json.load(f)

    return index, texts, metadatas


def retrieve_from_regulation(question: str, regulation: str, top_k: int = 4):
    index, texts, metadatas = load_regulation_store(regulation)

    query_embedding = model.encode([question], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx == -1:
            continue

        results.append({
            "text": texts[idx],
            "metadata": metadatas[idx]
        })

    return results


def retrieve(question: str, regulations: list[str], top_k_per_regulation: int = 4):
    merged = []

    for reg in regulations:
        merged.extend(retrieve_from_regulation(question, reg, top_k=top_k_per_regulation))

    return merged