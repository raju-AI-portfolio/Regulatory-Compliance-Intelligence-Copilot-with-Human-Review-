import re
from openai import OpenAI
from app.core.config import settings


def normalize_gdpr_citations(text: str) -> str:
    if not text:
        return text

    text = re.sub(
        r"\bGDPR\s+(\d+)\((\d+)\)",
        r"GDPR Art. \1(\2)",
        text
    )

    text = re.sub(
        r"\bGDPR\s+(?!Art\.)(?!p\.)(\d+)\b",
        r"GDPR Art. \1",
        text
    )

    return text


def simplify_citation_group(content: str) -> str:
    parts = [p.strip() for p in content.split(";") if p.strip()]

    unique_parts = []
    for p in parts:
        if p not in unique_parts:
            unique_parts.append(p)

    subsection_articles = set()
    for p in unique_parts:
        sub_match = re.fullmatch(r"GDPR Art\. (\d+)\((\d+)\)", p)
        if sub_match:
            subsection_articles.add(sub_match.group(1))

    filtered_parts = []
    for p in unique_parts:
        broad_match = re.fullmatch(r"GDPR Art\. (\d+)", p)
        if broad_match and broad_match.group(1) in subsection_articles:
            continue
        filtered_parts.append(p)

    has_gdpr_article = any(re.fullmatch(r"GDPR Art\. \d+(\(\d+\))?", p) for p in filtered_parts)
    if has_gdpr_article:
        filtered_parts = [p for p in filtered_parts if not re.fullmatch(r"GDPR p\.\d+", p)]

    return "; ".join(filtered_parts)


def clean_parenthetical_citations(text: str) -> str:
    if not text:
        return text

    lines = text.splitlines()
    cleaned_lines = []

    pattern = re.compile(r"\((.*?)\)([.,]?)$")

    for line in lines:
        stripped = line.rstrip()
        match = pattern.search(stripped)

        if match:
            citation_group = match.group(1)
            trailing_punct = match.group(2)
            cleaned_group = simplify_citation_group(citation_group)
            stripped = pattern.sub(f"({cleaned_group}){trailing_punct}", stripped)

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)


def postprocess_answer_text(text: str) -> str:
    if not text:
        return text

    text = normalize_gdpr_citations(text)
    text = clean_parenthetical_citations(text)
    return text


def build_context(retrieved_chunks):
    context_parts = []

    for i, item in enumerate(retrieved_chunks, start=1):
        metadata = item.get("metadata", {}) or {}

        citation = metadata.get("citation", "Unknown citation")
        source_document = metadata.get("source_document", "Unknown source")
        regulation = metadata.get("regulation", item.get("regulation", "Unknown regulation"))
        text = metadata.get("text", item.get("text", ""))

        article_number = metadata.get("article_number", "")
        section_number = metadata.get("section_number", "")
        page_number = metadata.get("page_number", "")
        source_type = metadata.get("source_type", "")
        title = metadata.get("title", metadata.get("article_title", ""))

        context_parts.append(
            f"[Source {i}]\n"
            f"Regulation: {regulation}\n"
            f"Document: {source_document}\n"
            f"Citation: {citation}\n"
            f"Article Number: {article_number}\n"
            f"Section Number: {section_number}\n"
            f"Page Number: {page_number}\n"
            f"Source Type: {source_type}\n"
            f"Title: {title}\n"
            f"Text:\n{text}\n"
        )

    return "\n\n".join(context_parts)


def is_comparison_question(question: str) -> bool:
    q = question.lower()

    comparison_terms = [
        "compare",
        "comparison",
        "difference",
        "differences",
        "different",
        "vs",
        "versus",
        "across frameworks",
        "across regulations",
        "gdpr and hipaa",
        "hipaa and gdpr",
        "gdpr vs hipaa",
        "hipaa vs gdpr",
        "gdpr and nist",
        "nist and gdpr",
        "hipaa and nist",
        "nist and hipaa",
    ]

    return any(term in q for term in comparison_terms)


def get_regulations_from_chunks(retrieved_chunks):
    ordered = []
    seen = set()

    for item in retrieved_chunks:
        regulation = (item.get("regulation") or item.get("metadata", {}).get("regulation") or "").upper()
        if regulation and regulation not in seen:
            ordered.append(regulation)
            seen.add(regulation)

    return ordered


def generate_answer(question: str, retrieved_chunks):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    context = build_context(retrieved_chunks)
    regulations = get_regulations_from_chunks(retrieved_chunks)
    comparison_mode = is_comparison_question(question)
    multi_framework = len(regulations) >= 2

    prompt = f"""
You are a regulatory compliance assistant.

Answer the user's question using ONLY the provided sources.
If the answer is not clearly supported by the sources, say exactly:
"Not found in the provided sources."

Be precise. Do not invent facts.
Closely paraphrase only what is supported by the source text.
Do not merge different regulations into one blended rule unless the sources explicitly support that.

Detected regulations in the retrieved sources:
{", ".join(regulations) if regulations else "Unknown"}

Comparison mode:
{comparison_mode}

Citation rules:
- Use consistent citation formatting inside the answer.
- For GDPR, prefer article-based citations when available.
  Examples:
  - GDPR Art. 7(3)
  - GDPR Art. 13(2)
  - GDPR Art. 14(2)
  - GDPR Art. 7
- For HIPAA, prefer section-based citations when available.
  Examples:
  - HIPAA 45 CFR § 164.502
  - HIPAA 45 CFR § 164.506
  - HIPAA 45 CFR § 164.508
  - HIPAA 45 CFR § 164.512
  - HIPAA 45 CFR § 164.514
- For NIST, prefer control ID or section citations when available.
- Use page citations only when no better structured citation is available.
- Do not mix multiple citation styles for the same point unless necessary.

Special guidance for HIPAA answers:
- For broad HIPAA questions about uses and disclosures of protected health information, organize the answer around:
  1. the general rule / baseline restriction under HIPAA 45 CFR § 164.502
  2. treatment, payment, and health care operations under HIPAA 45 CFR § 164.506
  3. authorization-required situations under HIPAA 45 CFR § 164.508
  4. specific permitted disclosures without authorization under HIPAA 45 CFR § 164.512
  5. additional disclosure-related requirements such as de-identification under HIPAA 45 CFR § 164.514

Formatting rules:
- Keep the answer concise and professional.
- Do NOT add a separate "Citations" section at the end.
- If only one regulation is relevant, short bullet points are fine.
- If more than one regulation is relevant, DO NOT use generic mixed bullets.

Multi-framework formatting rules:
- When more than one regulation is relevant, structure the answer exactly like this:
  Under GDPR:
  - ...
  - ...

  Under HIPAA:
  - ...
  - ...

  Under NIST:
  - ...
  - ...

  Key overlap:
  - ...

  Key difference:
  - ...

- Include only the sections that are supported by the provided sources.
- If a regulation is not actually supported by the retrieved sources, omit that section.
- "Key overlap" must mention only genuinely supported common themes.
- "Key difference" must mention only genuinely supported distinctions.
- If the question is a comparison question, always prefer the sectioned format above.
- Do not collapse GDPR consent and HIPAA authorization into one undifferentiated summary paragraph.

User question:
{question}

Provided sources:
{context}
"""

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You answer only from supplied compliance sources and keep different regulations clearly separated when multiple frameworks are involved."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content or ""
    answer = postprocess_answer_text(answer)

    return answer