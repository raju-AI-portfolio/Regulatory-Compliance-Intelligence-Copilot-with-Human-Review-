from app.core.config import settings
from ingestion.notion.json_loader import load_structured_json
from ingestion.notion.json_mapper import map_structured_record
from ingestion.pdf.embedder import get_embedding_model, embed_texts
from ingestion.pdf.upsert_pinecone import (
    get_pinecone_index,
    build_pinecone_records,
    upsert_records,
)

JSON_PATH = "data/structured/gdpr_articles.json"
NAMESPACE = "gdpr_structured"


def main():
    print(f"Loading structured GDPR JSON from {JSON_PATH}")
    records = load_structured_json(JSON_PATH)
    print(f"Loaded {len(records)} structured records")

    mapped_chunks = []
    for record in records:
        metadata = map_structured_record(record, namespace=NAMESPACE)
        mapped_chunks.append({
            "text": record.get("text", ""),
            "metadata": metadata,
        })

    texts = [item["text"] for item in mapped_chunks]

    print("Loading embedding model...")
    model = get_embedding_model("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    embeddings = embed_texts(texts, model)

    print("Connecting to Pinecone...")
    index = get_pinecone_index(
        api_key=settings.PINECONE_API_KEY,
        index_name=settings.PINECONE_INDEX_NAME,
    )

    print("Building Pinecone records...")
    pinecone_records = build_pinecone_records(mapped_chunks, embeddings, namespace=NAMESPACE)
    print(f"Built {len(pinecone_records)} Pinecone records")

    print("Upserting records to Pinecone...")
    upsert_records(index, pinecone_records, namespace=NAMESPACE)

    print(f"Finished ingesting {len(pinecone_records)} records into namespace: {NAMESPACE}")


if __name__ == "__main__":
    main()
