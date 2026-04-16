def route_question(question: str):
    q = question.lower()
    regs = []

    eu_words = ["gdpr", "europe", "eu", "european", "cross-border", "germany", "france"]
    us_words = ["hipaa", "us", "united states", "phi", "ephi", "patient", "hospital"]
    security_words = ["nist", "security", "access control", "encryption", "technical safeguard"]

    if any(word in q for word in eu_words):
        regs.append("GDPR")

    if any(word in q for word in us_words):
        regs.append("HIPAA")

    if any(word in q for word in security_words):
        regs.append("NIST")

    if not regs:
        regs = ["GDPR", "HIPAA"]

    return regs