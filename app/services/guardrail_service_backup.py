import re


INJECTION_PATTERNS = [
    r"ignore (all|any|the)?\s*previous instructions",
    r"ignore your instructions",
    r"disregard previous instructions",
    r"forget previous instructions",
    r"reveal (your|the)?\s*(system|hidden|developer) prompt",
    r"show (your|the)?\s*(system|hidden|developer) prompt",
    r"what is (your|the)?\s*(system|hidden|developer) prompt",
    r"what are (your|the)?\s*(hidden|developer) instructions",
    r"jailbreak",
    r"bypass (your|the) rules",
    r"act as (an )?(unrestricted|uncensored|evil) assistant",
    r"developer message",
    r"system message",
    r"prompt injection",
]

UNSAFE_PATTERNS = [
    r"\bmalware\b",
    r"\bransomware\b",
    r"\bphishing\b",
    r"\bkeylogger\b",
    r"\bcredential theft\b",
    r"\bexploit\b",
    r"\bhack\b",
    r"\bbypass security\b",
    r"\bsteal passwords\b",
    r"\bbomb\b",
    r"\bweapon\b",
    r"\bpoison\b",
]

ALLOWED_COMPLIANCE_TERMS = [
    "gdpr",
    "hipaa",
    "nist",
    "privacy",
    "security rule",
    "privacy rule",
    "breach notification",
    "consent",
    "authorization",
    "personal data",
    "personal data breach",
    "protected health information",
    "phi",
    "ephi",
    "controller",
    "processor",
    "data subject",
    "cybersecurity framework",
    "csf",
    "800-53",
    "risk management",
    "safeguard",
    "safeguards",
    "compliance",
    "regulation",
    "regulatory",
    "lawful basis",
    "disclosure",
    "retention",
    "patient data",
    "health data",
    "review",
    "audit",
    "security incident",
    "incident response",
    "breach",
    "data breach",
    "security controls",
    "administrative safeguards",
    "physical safeguards",
    "technical safeguards",
    "access control",
    "encryption",
    "supervisory authority",
]


def detect_prompt_injection(question: str) -> bool:
    q = question.lower().strip()
    return any(re.search(pattern, q) for pattern in INJECTION_PATTERNS)


def detect_unsafe_content(question: str) -> bool:
    q = question.lower().strip()
    return any(re.search(pattern, q) for pattern in UNSAFE_PATTERNS)


def detect_off_topic(question: str) -> bool:
    q = question.lower().strip()

    if any(term in q for term in ALLOWED_COMPLIANCE_TERMS):
        return False

    off_topic_patterns = [
        r"\bwrite a poem\b",
        r"\btell me a joke\b",
        r"\bmovie recommendation\b",
        r"\brecipe\b",
        r"\bweather\b",
        r"\bcricket score\b",
        r"\bipl\b",
        r"\bfootball score\b",
        r"\btranslate this\b",
        r"\bwho won\b",
        r"\bstock tip\b",
    ]

    if any(re.search(pattern, q) for pattern in off_topic_patterns):
        return True

    return False


def evaluate_question_guardrails(question: str) -> dict:
    if not question or not question.strip():
        return {
            "allowed": False,
            "reason": "empty_input",
            "message": "No question was provided.",
        }

    if detect_prompt_injection(question):
        return {
            "allowed": False,
            "reason": "prompt_injection",
            "message": "This request was blocked because it appears to contain prompt-injection or jailbreak-style instructions.",
        }

    if detect_unsafe_content(question):
        return {
            "allowed": False,
            "reason": "unsafe_request",
            "message": "This request was blocked because it appears to ask for unsafe or disallowed content.",
        }

    if detect_off_topic(question):
        return {
            "allowed": False,
            "reason": "off_topic",
            "message": "This assistant only supports regulatory compliance questions related to frameworks such as GDPR, HIPAA, and NIST.",
        }

    return {
        "allowed": True,
        "reason": "allowed",
        "message": "",
    }