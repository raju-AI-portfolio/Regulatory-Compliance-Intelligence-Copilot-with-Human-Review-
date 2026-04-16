from typing import List, Dict
from pinecone import Pinecone


def get_pinecone_index(api_key: str, index_name: str):
    pc = Pinecone(api_key=api_key)
    return pc.Index(index_name)


def build_pinecone_records(chunks: List[Dict], embeddings, namespace: str) -> List[Dict]:
    records = []

    for chunk, embedding in zip(chunks, embeddings):
        metadata = chunk["metadata"]

        records.append({
            "id": metadata["chunk_id"],
            "values": embedding.tolist(),
            "metadata": metadata,
        })

    return records


def upsert_records(index, records: List[Dict], namespace: str, batch_size: int = 100):
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)
