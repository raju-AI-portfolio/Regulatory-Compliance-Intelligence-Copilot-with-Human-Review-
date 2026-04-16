def calculate_confidence(reranked_chunks: list, citations: str = "") -> float:
    if not reranked_chunks:
        return 0.0

    top_chunks = reranked_chunks[:5]

    rerank_scores = [item.get("rerank_score", 0.0) for item in top_chunks]
    top_score = rerank_scores[0] if rerank_scores else 0.0
    avg_top_scores = sum(rerank_scores) / len(rerank_scores) if rerank_scores else 0.0

    citation_count = len([c.strip() for c in citations.split(",") if c.strip()]) if citations else 0

    regulations = []
    namespaces = []

    for item in top_chunks:
        regulation = (item.get("regulation") or "").upper()
        namespace = item.get("namespace") or ""

        if regulation:
            regulations.append(regulation)
        if namespace:
            namespaces.append(namespace)

    unique_regulations = sorted(set(regulations))
    unique_namespaces = sorted(set(namespaces))

    multi_framework = len(unique_regulations) >= 2

    confidence = top_score

    # Citation support bonus
    if citation_count >= 4:
        confidence += 0.14
    elif citation_count == 3:
        confidence += 0.11
    elif citation_count == 2:
        confidence += 0.08
    elif citation_count == 1:
        confidence += 0.04

    # Consistency bonus from top reranked chunks
    if avg_top_scores >= 0.55:
        confidence += 0.10
    elif avg_top_scores >= 0.45:
        confidence += 0.06
    elif avg_top_scores >= 0.30:
        confidence += 0.03

    # Bonus for evidence breadth across multiple chunks
    if len(top_chunks) >= 5:
        confidence += 0.04
    elif len(top_chunks) >= 3:
        confidence += 0.02

    # Bonus for source diversity
    if len(unique_namespaces) >= 2:
        confidence += 0.04

    # Special handling for cross-framework answers:
    # mixed-law questions often have lower rerank scores,
    # so reward balanced evidence across frameworks.
    if multi_framework:
        confidence += 0.12

        # If two or more frameworks appear in top chunks, add support bonus
        if len(unique_regulations) >= 2:
            confidence += 0.08

        # If average rerank is decent for cross-framework retrieval, reward it
        if avg_top_scores >= 0.25:
            confidence += 0.05

    return round(min(confidence, 0.95), 4)