import os
import json
import faiss
from sentence_transformers import SentenceTransformer

from app.config import PDF_FOLDER, INDEX_FOLDER, EMBEDDING_MODEL
from app.pdf_utils import extract_pages_from_pdf
from app.chunker import chunk_pages


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all_chunks():
    all_chunks = []

    for filename in os.listdir(PDF_FOLDER):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_FOLDER, filename)
        pages = extract_pages_from_pdf(pdf_path)
        chunks = chunk_pages(pages)
        all_chunks.extend(chunks)

    return all_chunks


def build_indexes():
    os.makedirs(INDEX_FOLDER, exist_ok=True)

    model = SentenceTransformer(EMBEDDING_MODEL)
    chunks = load_all_chunks()

    grouped = {}
    for chunk in chunks:
        regulation = chunk["metadata"]["regulation"]
        grouped.setdefault(regulation, []).append(chunk)

    for regulation, reg_chunks in grouped.items():
        texts = [c["text"] for c in reg_chunks]
        metadatas = [c["metadata"] for c in reg_chunks]

        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        embeddings = embeddings.astype("float32")

        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        reg_folder = os.path.join(INDEX_FOLDER, regulation.lower())
        os.makedirs(reg_folder, exist_ok=True)

        faiss.write_index(index, os.path.join(reg_folder, "index.faiss"))
        save_json(os.path.join(reg_folder, "texts.json"), texts)
        save_json(os.path.join(reg_folder, "metadatas.json"), metadatas)

        print(f"Built index for {regulation}: {len(texts)} chunks")


if __name__ == "__main__":
    build_indexes()