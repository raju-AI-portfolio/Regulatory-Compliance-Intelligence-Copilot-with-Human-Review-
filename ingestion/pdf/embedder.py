from typing import List
from sentence_transformers import SentenceTransformer


def get_embedding_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


def embed_texts(texts: List[str], model: SentenceTransformer):
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    return embeddings.astype("float32")
