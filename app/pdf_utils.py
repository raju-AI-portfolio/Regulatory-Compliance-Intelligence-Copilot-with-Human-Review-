import os
import re
from pypdf import PdfReader


def detect_regulation_from_filename(filename: str) -> str:
    name = filename.lower()

    if "gdpr" in name:
        return "GDPR"
    if "hipaa" in name:
        return "HIPAA"
    if "nist" in name:
        return "NIST"

    return "UNKNOWN"


def detect_jurisdiction(regulation: str) -> str:
    mapping = {
        "GDPR": "EU",
        "HIPAA": "US",
        "NIST": "GLOBAL",
    }
    return mapping.get(regulation, "UNKNOWN")


def detect_section_label(text: str, regulation: str) -> str:
    if regulation == "GDPR":
        match = re.search(r"(Article\s+\d+)", text, re.IGNORECASE)
        if match:
            return match.group(1)

    if regulation == "HIPAA":
        match = re.search(r"(§\s*\d+\.\d+)", text)
        if match:
            return match.group(1)

    if regulation == "NIST":
        match = re.search(r"\b([A-Z]{2,5}-\d+)\b", text)
        if match:
            return match.group(1)

    return ""


def extract_pages_from_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    filename = os.path.basename(pdf_path)
    regulation = detect_regulation_from_filename(filename)
    jurisdiction = detect_jurisdiction(regulation)

    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()

        if not text:
            continue

        section_label = detect_section_label(text, regulation)

        if section_label:
            if regulation == "HIPAA":
                citation = f"HIPAA 45 CFR {section_label}"
            else:
                citation = f"{regulation} {section_label}"
        else:
            citation = f"{regulation} p.{i + 1}"

        pages.append({
            "text": text,
            "metadata": {
                "source_file": filename,
                "page_number": i + 1,
                "regulation": regulation,
                "jurisdiction": jurisdiction,
                "section_label": section_label,
                "citation": citation,
            }
        })

    return pages