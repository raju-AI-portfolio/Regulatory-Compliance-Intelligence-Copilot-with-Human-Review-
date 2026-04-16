def map_hipaa_structured_record(record: dict, namespace: str = "hipaa_structured") -> dict:
    section_number = record.get("section_number", "")
    title = record.get("title", "")
    citation = record.get("citation", "")
    text = record.get("text", "")

    chunk_id = f"{section_number or title}".replace(" ", "_").replace(".", "").replace("-", "_").lower()

    metadata = {
        "text": text,
        "source_document": "hipaa_structured.json",
        "regulation": record.get("regulation", "HIPAA"),
        "jurisdiction": record.get("jurisdiction", "US"),
        "section_type": "section",
        "section_number": section_number,
        "section_title": record.get("section_title", ""),
        "page_number": None,
        "effective_date": None,
        "version": "current",
        "citation": citation,
        "source_type": record.get("source_type", "structured_json"),
        "namespace": namespace,
        "is_deprecated": False,
        "chunk_id": chunk_id,
        "title": title,
        "subpart": record.get("subpart", ""),
        "part": record.get("part", "164"),
    }

    return {k: v for k, v in metadata.items() if v is not None}