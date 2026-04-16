from typing import List, Dict
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.multi_query_service import generate_query_variants


NAMESPACE_MAP = {
    "GDPR": ["gdpr_pdf", "gdpr_structured"],
    "HIPAA": ["hipaa_structured", "hipaa_pdf"],
    "NIST": ["nist_csf_pdf", "nist_pdf"],
}


def normalize_regulations(regulations: List[str]) -> List[str]:
    if not regulations:
        return ["GDPR", "HIPAA", "NIST"]
    return [r.upper() for r in regulations if r]


def is_csf_question(question: str) -> bool:
    lower_q = question.lower()

    return any(term in lower_q for term in [
        "core functions",
        "cybersecurity framework",
        "nist csf",
        "csf",
        "identify",
        "protect",
        "detect",
        "respond",
        "recover",
        "govern",
        "implementation tiers",
        "tiers",
        "profiles",
        "subcategories",
    ])


def get_namespaces_for_regulation(regulation: str, question: str) -> List[str]:
    regulation = regulation.upper()

    if regulation == "NIST":
        if is_csf_question(question):
            return ["nist_csf_pdf", "nist_pdf"]
        return ["nist_pdf", "nist_csf_pdf"]

    return NAMESPACE_MAP.get(regulation, [])


def expand_query(question: str, regulations: List[str]) -> str:
    q = question.strip()
    upper_regs = normalize_regulations(regulations)
    lower_q = q.lower()

    if "HIPAA" in upper_regs:
        if "phi" in lower_q and "protected health information" not in lower_q:
            q = q + " protected health information HIPAA Privacy Rule individually identifiable health information"

    if "GDPR" in upper_regs:
        if "consent" in lower_q and "data subject" not in lower_q:
            q = q + " data subject consent controller processing personal data"

    if "NIST" in upper_regs:
        if "access control" in lower_q and "authorization" not in lower_q:
            q = q + " access control authorization logical access physical access"

        if is_csf_question(q):
            q = q + " NIST Cybersecurity Framework CSF core functions Govern Identify Protect Detect Respond Recover profiles implementation tiers subcategories"

    return q


def score_source_priority(question: str, regulation: str, metadata: Dict) -> float:
    """
    Add a lightweight boost for the most relevant source document / namespace
    based on question intent.

    HIPAA priority:
    - Structured HIPAA sections for privacy / uses-disclosures questions
    - Security Rule PDF for security questions
    - Breach Notification PDF for breach questions
    - Extra boost for the most important HIPAA sections for broad privacy questions

    NIST priority:
    - Prefer nist_csf_pdf for CSF questions
    - Boost chunks that mention CSF concepts/functions
    """
    lower_q = question.lower()
    upper_reg = regulation.upper()
    source_document = str(metadata.get("source_document", "")).lower()
    namespace = str(metadata.get("namespace", "")).lower()
    section_number = str(metadata.get("section_number", "")).replace("§", "").strip()
    text = str(metadata.get("text", "")).lower()

    boost = 0.0

    if upper_reg == "HIPAA":
        is_security_question = any(term in lower_q for term in [
            "security rule",
            "administrative safeguards",
            "physical safeguards",
            "technical safeguards",
            "access control",
            "audit controls",
            "integrity",
            "authentication",
            "transmission security",
            "ephi",
        ])

        is_breach_question = any(term in lower_q for term in [
            "breach",
            "breach notification",
            "compromised",
            "incident",
            "notification",
        ])

        is_privacy_question = any(term in lower_q for term in [
            "privacy rule",
            "phi",
            "protected health information",
            "individually identifiable health information",
            "uses and disclosures",
            "authorization",
            "treatment",
            "payment",
            "health care operations",
        ])

        if is_privacy_question:
            if "hipaa_structured" in namespace:
                boost += 0.12
            if "part_164" in source_document:
                boost += 0.03
            if "breach" in source_document:
                boost -= 0.02

            if section_number == "164.502":
                boost += 0.10
            elif section_number == "164.506":
                boost += 0.14
            elif section_number == "164.508":
                boost += 0.08
            elif section_number == "164.512":
                boost += 0.07
            elif section_number == "164.514":
                boost += 0.04
            elif section_number == "164.522":
                boost -= 0.02

        if is_security_question:
            if "security" in source_document:
                boost += 0.08
            if "hipaa_structured" in namespace:
                boost -= 0.01
            if "breach" in source_document:
                boost -= 0.05

        if is_breach_question:
            if "breach" in source_document:
                boost += 0.08
            if "security" in source_document:
                boost -= 0.03
            if "hipaa_structured" in namespace:
                boost -= 0.01

    if upper_reg == "NIST":
        csf_question = is_csf_question(question)

        if csf_question:
            if namespace == "nist_csf_pdf":
                boost += 0.18
            elif namespace == "nist_pdf":
                boost += 0.03

            matched_terms = 0
            for term in ["govern", "identify", "protect", "detect", "respond", "recover"]:
                if term in text:
                    matched_terms += 1

            boost += matched_terms * 0.04

            if "framework" in text and "cybersecurity" in text:
                boost += 0.06

            if "csf" in text:
                boost += 0.04

            if "profile" in text or "profiles" in text:
                boost += 0.03

            if "tier" in text or "tiers" in text:
                boost += 0.03

        else:
            if namespace == "nist_pdf":
                boost += 0.05

    return boost


EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def get_query_embedding(question: str):
    embedding = EMBEDDING_MODEL.encode(question, convert_to_numpy=True)
    return embedding.astype("float32").tolist()


def get_pinecone_index():
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return pc.Index(settings.PINECONE_INDEX_NAME)


def retrieve_chunks(question: str, regulations: List[str], top_k: int = 5) -> List[Dict]:
    index = get_pinecone_index()
    regulations = normalize_regulations(regulations)
    expanded_question = expand_query(question, regulations)
    query_vector = get_query_embedding(expanded_question)

    all_matches = []

    for regulation in regulations:
        namespaces = get_namespaces_for_regulation(regulation, question)
        for namespace in namespaces:
            result = index.query(
                vector=query_vector,
                top_k=top_k,
                namespace=namespace,
                include_metadata=True,
            )

            matches = result.get("matches", [])
            for match in matches:
                metadata = match.get("metadata", {})
                base_score = match.get("score", 0.0)

                metadata["namespace"] = namespace

                priority_boost = score_source_priority(question, regulation, metadata)
                final_score = base_score + priority_boost

                all_matches.append({
                    "regulation": regulation,
                    "namespace": namespace,
                    "score": final_score,
                    "base_score": base_score,
                    "priority_boost": priority_boost,
                    "text": metadata.get("text", ""),
                    "metadata": metadata,
                })

    all_matches.sort(key=lambda x: x["score"], reverse=True)
    return all_matches[:top_k]


def retrieve_chunks_multi_query(question: str, regulations: List[str], top_k: int = 5) -> List[Dict]:
    index = get_pinecone_index()
    regulations = normalize_regulations(regulations)
    query_variants = generate_query_variants(question, regulations)

    all_matches = []
    seen_chunk_ids = set()

    for query_variant in query_variants:
        expanded_question = expand_query(query_variant, regulations)
        query_vector = get_query_embedding(expanded_question)

        for regulation in regulations:
            namespaces = get_namespaces_for_regulation(regulation, question)
            for namespace in namespaces:
                result = index.query(
                    vector=query_vector,
                    top_k=top_k,
                    namespace=namespace,
                    include_metadata=True,
                )

                matches = result.get("matches", [])
                for match in matches:
                    metadata = match.get("metadata", {})
                    chunk_id = metadata.get("chunk_id") or f"{namespace}:{metadata.get('text', '')[:100]}"

                    if chunk_id in seen_chunk_ids:
                        continue

                    seen_chunk_ids.add(chunk_id)

                    base_score = match.get("score", 0.0)

                    metadata["namespace"] = namespace

                    priority_boost = score_source_priority(question, regulation, metadata)
                    final_score = base_score + priority_boost

                    all_matches.append({
                        "regulation": regulation,
                        "namespace": namespace,
                        "score": final_score,
                        "base_score": base_score,
                        "priority_boost": priority_boost,
                        "text": metadata.get("text", ""),
                        "metadata": metadata,
                    })

    all_matches.sort(key=lambda x: x["score"], reverse=True)
    return all_matches[:top_k * 3]