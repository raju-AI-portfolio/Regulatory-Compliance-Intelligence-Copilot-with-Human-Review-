import re
import unicodedata


def make_ascii_id(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = value.replace(" ", "_")
    value = value.replace(".", "")
    value = value.replace("-", "_")
    value = re.sub(r"[^a-z0-9_]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def map_gdpr_csv_record(record: dict, namespace: str = "gdpr_structured") -> dict:
    article = str(record.get("article", "")).strip()
    article_title = str(record.get("article_title", "")).strip()
    sub_article = str(record.get("sub_article", "")).strip()
    chapter = str(record.get("chapter", "")).strip()
    chapter_title = str(record.get("chapter_title", "")).strip()
    text = str(record.get("gdpr_text", "")).strip()
    href = str(record.get("href", "")).strip()

    title = f"GDPR {article} - {article_title}"
    citation = f"GDPR {article}"
    if sub_article:
        citation = f"GDPR {article}({sub_article})"

    raw_id = f"{article}_{sub_article}_{article_title}"
    chunk_id = make_ascii_id(raw_id)

    metadata = {
        "text": text,
        "source_document": "gdpr_text.csv",
        "regulation": "GDPR",
        "jurisdiction": "EU",
        "section_type": "article",
        "section_number": sub_article,
        "section_title": chapter_title,
        "article_number": article,
        "article_title": article_title,
        "page_number": None,
        "effective_date": None,
        "version": "current",
        "citation": citation,
        "source_type": "structured_csv",
        "namespace": namespace,
        "is_deprecated": False,
        "chunk_id": chunk_id,
        "title": title,
        "chapter": chapter,
        "chapter_title": chapter_title,
        "href": href,
    }

    return {k: v for k, v in metadata.items() if v is not None}
