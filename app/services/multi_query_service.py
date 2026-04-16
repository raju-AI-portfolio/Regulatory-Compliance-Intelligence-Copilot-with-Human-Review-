from typing import List


def generate_query_variants(question: str, regulations: List[str]) -> List[str]:
    q = question.strip()
    variants = [q]

    lower_q = q.lower()
    upper_regs = [r.upper() for r in regulations]

    if "GDPR" in upper_regs:
        if "consent" in lower_q:
            variants.append(q + " data subject consent withdrawal controller")
            variants.append("GDPR consent withdrawal data subject rights")

        elif "breach" in lower_q or "notification" in lower_q:
            variants.append(q + " personal data breach supervisory authority data subject")
            variants.append("GDPR breach notification Article 33 Article 34")

    if "HIPAA" in upper_regs:
        if "safeguard" in lower_q or "security" in lower_q:
            variants.append(q + " administrative physical technical safeguards ePHI")
            variants.append("HIPAA Security Rule safeguards protected health information")

        elif "breach" in lower_q:
            variants.append(q + " breach notification protected health information covered entity")
            variants.append("HIPAA breach notification rule PHI")

    if "NIST" in upper_regs:
        if "access control" in lower_q:
            variants.append(q + " authorization logical access least privilege")
            variants.append("NIST access control identification authentication authorization")

        elif "cybersecurity framework" in lower_q or "core functions" in lower_q:
            variants.append(q + " identify protect detect respond recover")
            variants.append("NIST CSF identify protect detect respond recover")

    # deduplicate while preserving order
    seen = set()
    deduped = []
    for item in variants:
        if item not in seen:
            seen.add(item)
            deduped.append(item)

    return deduped[:3]