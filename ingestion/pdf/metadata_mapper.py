from typing import Dict


def map_chunk_metadata(chunk: Dict, namespace: str, source_type: str = "pdf") -> Dict:
    metadata = chunk["metadata"]

    mapped = {
        "text": chunk.get("text", ""),
        "source_document": metadata.get("source_file"),
        "regulation": metadata.get("regulation"),
        "jurisdiction": metadata.get("jurisdiction"),
        "section_type": "section",
        "section_number": metadata.get("section_label"),
        "section_title": None,
        "article_number": metadata.get("section_label") if metadata.get("regulation") == "GDPR" else None,
        "article_title": None,
        "page_number": metadata.get("page_number"),
        "effective_date": None,
        "version": "current",
        "citation": metadata.get("citation"),
        "source_type": source_type,
        "namespace": namespace,
        "is_deprecated": False,
        "chunk_id": metadata.get("chunk_id"),
    }

    return {k: v for k, v in mapped.items() if v is not None}
