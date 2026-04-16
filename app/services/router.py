from typing import List


def detect_regulations(question: str) -> List[str]:
    q = question.lower().strip()
    matched = []

    gdpr_terms = [
        "gdpr",
        "eu privacy",
        "general data protection regulation",
        "data subject",
        "controller",
        "processor",
        "lawful basis",
        "personal data",
        "consent withdrawal",
        "right to erasure",
        "right to be forgotten",
        "eu",
        "european union",
    ]

    hipaa_terms = [
        "hipaa",
        "phi",
        "protected health information",
        "ephi",
        "covered entity",
        "business associate",
        "privacy rule",
        "security rule",
        "breach notification",
        "45 cfr 164",
        "authorization",
        "treatment payment healthcare operations",
    ]

    nist_terms = [
        "nist",
        "cybersecurity framework",
        "nist csf",
        "csf",
        "800-53",
        "risk management framework",
        "rmf",
        "identify protect detect respond recover",
        "implementation tiers",
        "profiles",
        "subcategories",
        "govern",
    ]

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
        "which regulation",
        "which framework",
        "gdpr and hipaa",
        "hipaa and gdpr",
        "gdpr vs hipaa",
        "hipaa vs gdpr",
        "gdpr and nist",
        "nist and gdpr",
        "hipaa and nist",
        "nist and hipaa",
    ]

    healthcare_terms = [
        "patient",
        "hospital",
        "medical",
        "healthcare",
        "clinic",
        "doctor",
        "provider",
        "payer",
        "health plan",
    ]

    privacy_terms = [
        "privacy",
        "personal data",
        "consent",
        "breach",
        "data retention",
        "data sharing",
        "disclosure",
        "access request",
        "deletion",
    ]

    security_terms = [
        "security",
        "cybersecurity",
        "controls",
        "safeguards",
        "risk management",
        "access control",
        "incident response",
    ]

    gdpr_hit = any(term in q for term in gdpr_terms)
    hipaa_hit = any(term in q for term in hipaa_terms)
    nist_hit = any(term in q for term in nist_terms)
    comparison_hit = any(term in q for term in comparison_terms)

    if gdpr_hit:
        matched.append("GDPR")

    if hipaa_hit:
        matched.append("HIPAA")

    if nist_hit:
        matched.append("NIST")

    # If user explicitly asks to compare or distinguish frameworks,
    # preserve all relevant matches and infer missing likely pairings.
    if comparison_hit:
        if "privacy" in q or "consent" in q or "disclosure" in q:
            if "GDPR" not in matched:
                matched.append("GDPR")
            if any(term in q for term in healthcare_terms + ["phi", "hipaa", "patient"]):
                if "HIPAA" not in matched:
                    matched.append("HIPAA")

        if any(term in q for term in security_terms):
            if "NIST" not in matched and ("cyber" in q or "security" in q or "framework" in q):
                matched.append("NIST")

    if not matched:
        looks_healthcare = any(term in q for term in healthcare_terms)
        looks_privacy = any(term in q for term in privacy_terms)
        looks_security = any(term in q for term in security_terms)

        # Healthcare + privacy often needs HIPAA, sometimes alongside GDPR
        if looks_healthcare and looks_privacy:
            matched = ["HIPAA", "GDPR"]

        # General privacy without healthcare bias -> GDPR first
        elif looks_privacy:
            matched = ["GDPR"]

        # Security / controls / cyber -> NIST
        elif looks_security:
            matched = ["NIST"]

        # Pure healthcare without explicit privacy/security -> HIPAA
        elif looks_healthcare:
            matched = ["HIPAA"]

        else:
            matched = ["GDPR", "HIPAA", "NIST"]

    # Deduplicate while preserving order
    deduped = []
    seen = set()
    for item in matched:
        if item not in seen:
            deduped.append(item)
            seen.add(item)

    return deduped
