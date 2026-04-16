import os
import sys

from app.core.config import settings
from ingestion.pdf.loader import load_pdfs_from_folder
from ingestion.pdf.chunker import build_chunks_from_pages
from ingestion.pdf.metadata_mapper import map_chunk_metadata
from ingestion.pdf.embedder import get_embedding_model, embed_texts
from ingestion.pdf.upsert_pinecone import (
    get_pinecone_index,
    build_pinecone_records,
    upsert_records,
)


NAMESPACE_MAP = {
    "GDPR": "gdpr_pdf",
    "HIPAA": "hipaa_pdf",
    "NIST": "nist_pdf",
    "NIST_CSF": "nist_csf_pdf",
}


FOLDER_MAP = {
    "GDPR": "data/raw/gdpr",
    "HIPAA": "data/raw/hipaa",
    "NIST": "data/raw/nist",
    "NIST_CSF": "data/raw/nist_csf",
}


def main(regulation: str):
    regulation = regulation.upper()

    if regulation not in NAMESPACE_MAP:
        raise ValueError(f"Unsupported regulation: {regulation}")

    folder_path = FOLDER_MAP[regulation]
    namespace = NAMESPACE_MAP[regulation]

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    print(f"Loading PDFs for {regulation} from {folder_path}")
    pages = load_pdfs_from_folder(folder_path)
    print(f"Loaded {len(pages)} pages")

    chunks = build_chunks_from_pages(pages)
    print(f"Built {len(chunks)} chunks")

    normalized_chunks = []
    for chunk in chunks:
        normalized_metadata = map_chunk_metadata(
            chunk,
            namespace=namespace,
            source_type="pdf",
        )
        normalized_chunks.append(
            {
                "text": chunk["text"],
                "metadata": normalized_metadata,
            }
        )

    texts = [c["text"] for c in normalized_chunks]

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
    records = build_pinecone_records(
        normalized_chunks,
        embeddings,
        namespace=namespace,
    )
    print(f"Built {len(records)} Pinecone records")

    print("Upserting records to Pinecone...")
    upsert_records(index, records, namespace=namespace)

    print(f"Finished ingesting {len(records)} records into namespace: {namespace}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingestion/pdf/run_pdf_ingestion.py <GDPR|HIPAA|NIST|NIST_CSF>")
        sys.exit(1)

    main(sys.argv[1])