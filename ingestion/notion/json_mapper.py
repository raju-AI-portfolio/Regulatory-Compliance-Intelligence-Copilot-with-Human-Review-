def map_structured_record(record: dict, namespace: str = "gdpr_structured") -> dict:
    article_number = record.get("article_number", "")
    title = record.get("title", "")
    citation = record.get("citation", "")
    text = record.get("text", "")

    chunk_id = f"{article_number or title}".replace(" ", "_").replace(".", "").replace("-", "_").lower()

    metadata = {
        "text": text,
        "source_document": "gdpr_articles.json",
        "regulation": record.get("regulation", "GDPR"),
        "jurisdiction": record.get("jurisdiction", "EU"),
        "section_type": "article",
        "section_number": record.get("section_number", ""),
        "section_title": record.get("section_title", ""),
        "article_number": article_number,
        "article_title": record.get("article_title", ""),
        "page_number": None,
        "effective_date": None,
        "version": "current",
        "citation": citation,
        "source_type": record.get("source_type", "structured_json"),
        "namespace": namespace,
        "is_deprecated": False,
        "chunk_id": chunk_id,
        "title": title,
    }

    return {k: v for k, v in metadata.items() if v is not None}
