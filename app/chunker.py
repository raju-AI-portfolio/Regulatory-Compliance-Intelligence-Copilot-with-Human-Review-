import re


def split_text(text: str, chunk_size: int = 1000, overlap: int = 150):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def normalize_section_label(section_label: str) -> str:
    if not section_label:
        return ""

    cleaned = re.sub(r"\s+", " ", section_label).strip()
    cleaned = re.sub(r"^§\s*", "§ ", cleaned)

    return cleaned


def is_toc_like_chunk(text: str, regulation: str) -> bool:
    if regulation != "HIPAA":
        return False

    normalized = re.sub(r"\s+", " ", text).strip()

    section_hits = re.findall(r"§\s*164\.\d+", normalized)
    if len(section_hits) >= 4:
        return True

    toc_signals = [
        "subpart e privacy of individually identifiable health information",
        "table of contents",
        "§ 164.501 definitions.",
        "§ 164.502 uses and disclosures of protected health information: general rules.",
        "§ 164.504 uses and disclosures: organizational requirements.",
        "§ 164.506 uses and disclosures to carry out treatment, payment, or health care operations.",
        "§ 164.508 uses and disclosures for which an authorization is required.",
    ]

    lowered = normalized.lower()
    signal_count = sum(1 for signal in toc_signals if signal in lowered)

    return signal_count >= 3


def detect_chunk_section_label(text: str, regulation: str) -> str:
    if regulation == "GDPR":
        match = re.search(r"^\s*(Article\s+\d+)\b", text, re.IGNORECASE | re.MULTILINE)
        if match:
            return normalize_section_label(match.group(1))

        match = re.search(r"(Article\s+\d+)\b", text, re.IGNORECASE)
        if match:
            return normalize_section_label(match.group(1))

    if regulation == "HIPAA":
        match = re.search(
            r"^\s*(§\s*164\.\d+)\s+[A-Z][^\n]{3,}",
            text,
            re.MULTILINE
        )
        if match:
            return normalize_section_label(match.group(1))

        match = re.search(r"^\s*(§\s*164\.\d+)\b", text, re.MULTILINE)
        if match:
            return normalize_section_label(match.group(1))

        match = re.search(r"\b45\s*CFR\s*(164\.\d+)\b", text, re.IGNORECASE)
        if match:
            return normalize_section_label(f"§ {match.group(1)}")

        return ""

    if regulation == "NIST":
        match = re.search(r"\b([A-Z]{2,5}-\d+)\b", text)
        if match:
            return normalize_section_label(match.group(1))

    return ""


def build_chunk_citation(
    regulation: str,
    section_label: str,
    page_number: int,
    source_file: str = "",
) -> str:
    source_file_lower = source_file.lower()

    if section_label:
        if regulation == "HIPAA":
            return f"HIPAA 45 CFR {section_label}"
        return f"{regulation} {section_label}"

    if regulation == "NIST" and source_file_lower == "nist.cswp.29.pdf":
        return f"NIST CSF 2.0 p.{page_number}"

    return f"{regulation} p.{page_number}"


def chunk_pages(pages, chunk_size: int = 1000, overlap: int = 150):
    all_chunks = []

    for page in pages:
        text = page["text"]
        metadata = page["metadata"]

        regulation = metadata.get("regulation", "UNKNOWN")
        page_number = metadata.get("page_number")
        page_level_section = normalize_section_label(metadata.get("section_label", ""))
        source_file = metadata.get("source_file", "")

        chunks = split_text(text, chunk_size=chunk_size, overlap=overlap)

        current_section = page_level_section

        for idx, chunk in enumerate(chunks):
            if is_toc_like_chunk(chunk, regulation):
                continue

            chunk_section_label = detect_chunk_section_label(chunk, regulation)

            if chunk_section_label:
                current_section = chunk_section_label

            final_section_label = current_section
            final_citation = build_chunk_citation(
                regulation=regulation,
                section_label=final_section_label,
                page_number=page_number,
                source_file=source_file,
            )

            all_chunks.append({
                "text": chunk,
                "metadata": {
                    **metadata,
                    "section_label": final_section_label,
                    "citation": final_citation,
                    "chunk_id": f'{metadata["source_file"]}_p{metadata["page_number"]}_c{idx + 1}'
                }
            })

    return all_chunks