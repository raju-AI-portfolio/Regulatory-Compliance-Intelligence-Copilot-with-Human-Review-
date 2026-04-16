def needs_human_review(
    answer: str,
    reranked_chunks: list,
    confidence: float = 1.0,
    confidence_threshold: float = 0.8,
    min_rerank_score: float = 0.2,
):
    if not reranked_chunks:
        return True

    regulations = []
    for item in reranked_chunks[:5]:
        regulation = (item.get("regulation") or "").upper()
        if regulation:
            regulations.append(regulation)

    unique_regulations = sorted(set(regulations))
    multi_framework = len(unique_regulations) >= 2

    effective_confidence_threshold = confidence_threshold
    effective_min_rerank_score = min_rerank_score

    # Mixed-framework answers usually have lower rerank scores because
    # evidence is split across regulations, so use a slightly lower threshold.
    if multi_framework:
        effective_confidence_threshold = 0.7
        effective_min_rerank_score = 0.18

    if confidence < effective_confidence_threshold:
        return True

    if not answer:
        return True

    lowered_answer = answer.lower()
    unsupported_signals = [
        "not found in the provided sources",
        "not sufficiently supported",
        "insufficiently supported",
    ]
    if any(signal in lowered_answer for signal in unsupported_signals):
        return True

    top_score = reranked_chunks[0].get("rerank_score", 0)
    if top_score < effective_min_rerank_score:
        return True

    return False


def get_review_status(needs_review: bool) -> str:
    return "pending_review" if needs_review else "generated"