import json
import re
from openai import OpenAI

from app.config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(chunks):
    blocks = []

    for i, chunk in enumerate(chunks, start=1):
        metadata = chunk.get("metadata", {}) or {}

        citation = metadata.get("citation", "N/A")
        source_file = metadata.get("source_file", metadata.get("source_document", "N/A"))
        page_number = metadata.get("page_number", "N/A")
        article_number = metadata.get("article_number", "")
        section_number = metadata.get("section_number", "")
        regulation = metadata.get("regulation", chunk.get("regulation", ""))
        source_type = metadata.get("source_type", "")
        section_type = metadata.get("section_type", "")
        title = metadata.get("title", metadata.get("article_title", ""))

        blocks.append(
            f"[Chunk {i}]\n"
            f"Regulation: {regulation}\n"
            f"Citation: {citation}\n"
            f"Article Number: {article_number}\n"
            f"Section Number: {section_number}\n"
            f"Section Type: {section_type}\n"
            f"Title: {title}\n"
            f"Source Type: {source_type}\n"
            f"Source File: {source_file}\n"
            f"Page: {page_number}\n"
            f"Text: {chunk.get('text', '')}\n"
        )

    return "\n\n".join(blocks)


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


def normalize_citations_array(citations: list) -> list:
    if not isinstance(citations, list):
        return citations

    normalized = []
    seen = set()

    for c in citations:
        citation = str(c).strip()
        citation = normalize_gdpr_citations(citation)

        if citation and citation not in seen:
            seen.add(citation)
            normalized.append(citation)

    return normalized


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
        "how do",
        "how does",
        "which regulation",
        "which framework",
        "gdpr and hipaa",
        "hipaa and gdpr",
        "gdpr vs hipaa",
        "hipaa vs gdpr",
        "hipaa and nist",
        "nist and hipaa",
        "gdpr and nist",
        "nist and gdpr",
    ]

    return any(term in q for term in comparison_terms)


def generate_answer(question: str, chunks: list, regulations: list[str]):
    context = build_context(chunks)
    comparison_mode = is_comparison_question(question)

    system_prompt = """
You are a compliance assistant.

Answer ONLY from the provided chunks.
Do not invent facts.
Do not merge frameworks into one blended rule unless the chunks explicitly support that.
If the chunks do not support an answer, say that the answer is not sufficiently supported.

Return valid JSON only with these keys:
{
  "final_answer": "...",
  "recommended_action": "...",
  "risk_note": "...",
  "citations": ["...", "..."],
  "confidence": 0.0
}

General formatting rules for final_answer:
- Keep the answer concise but professional.
- Mention exact citations inside the text when relevant.
- Use consistent citation style within the answer.
- Do not overload the answer with too many citations for every sentence.
- Never imply that one framework legally replaces another unless the chunks explicitly say so.

Single-framework answer rules:
- If one regulation applies, answer directly under that framework.

Multi-framework answer rules:
- If more than one regulation applies, separate clearly with headings:
  "Under GDPR:"
  "Under HIPAA:"
  "Under NIST:"
- For each framework, summarize only what the provided chunks support.
- If a framework is selected but weakly supported by the retrieved chunks, say so briefly.

Comparison answer rules:
- If the question is comparative, structure the final_answer in this order:
  1. "Under GDPR:"
  2. "Under HIPAA:"
  3. "Under NIST:" (only if relevant)
  4. "Key overlap:"
  5. "Key difference:"
- "Key overlap" should mention only supported common themes.
- "Key difference" should mention only supported distinctions.
- Do not force overlap or difference if not supported by the chunks.

Citation style rules:
- For GDPR, prefer article-based citations:
  - GDPR Art. 7(3)
  - GDPR Art. 13(2)
  - GDPR Art. 14(2)
  - GDPR Art. 7
- For HIPAA, prefer section-based citations when available:
  - HIPAA 45 CFR § 164.308
  - HIPAA 45 CFR § 164.312
  - HIPAA 45 CFR § 164.404
- For NIST, prefer control ID or section citations when available:
  - NIST AC-2
  - NIST IA-5
  - NIST AU-6
  - NIST CSF 2.0 p.8
- Use page numbers only when no better structured citation is available.

Recommended action rules:
- For multi-framework questions, recommended_action should tell the user to evaluate obligations framework-by-framework before operationalizing one combined policy.
- If the answer is partially supported, recommend legal/compliance validation or human review.

Risk note rules:
- For multi-framework questions, risk_note should mention the risk of applying one framework’s language to another without confirming scope, jurisdiction, and entity type.

Confidence scoring:
- 0.9 to 1.0: directly supported by clear, relevant chunks
- 0.7 to 0.89: mostly supported but some ambiguity remains
- below 0.7: weak support or incomplete evidence
"""

    user_prompt = f"""
Question:
{question}

Regulations selected:
{", ".join(regulations)}

Comparison mode:
{comparison_mode}

Retrieved chunks:
{context}

Important instruction:
When drafting the final_answer, normalize citations using metadata in the chunks.

For GDPR:
- If article_number and section_number are available, cite as GDPR Art. X(Y)
- If only article_number is available, cite as GDPR Art. X
- Use page citations only when article citation is unavailable

For HIPAA:
- Prefer section citations when available from metadata
- Do not convert HIPAA into GDPR-style article citations

For NIST:
- Preserve NIST control citations or NIST CSF 2.0 page citations when available

For multi-framework questions:
- Do not collapse GDPR, HIPAA, and NIST into one generic answer
- Keep each framework separate
- Then add overlap/difference only if supported by the retrieved chunks
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    content = response.choices[0].message.content
    result = json.loads(content)

    if "final_answer" in result and isinstance(result["final_answer"], str):
        result["final_answer"] = normalize_gdpr_citations(result["final_answer"])

    if "citations" in result:
        result["citations"] = normalize_citations_array(result["citations"])

    return result