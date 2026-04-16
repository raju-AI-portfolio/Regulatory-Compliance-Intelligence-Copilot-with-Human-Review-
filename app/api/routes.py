import requests

from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import QueryRequest
from app.services.audit_service import (
    get_latest_review_result_by_user_id,
    get_review_result_by_record_id,
    log_query_result,
)
from app.services.confidence_service import calculate_confidence
from app.services.generator import generate_answer
from app.services.guardrail_service import evaluate_question_guardrails
from app.services.reranker import rerank_chunks
from app.services.retriever import retrieve_chunks, retrieve_chunks_multi_query
from app.services.review_service import get_review_status, needs_human_review
from app.services.router import detect_regulations

router = APIRouter()
ENABLE_MULTI_QUERY = True


def send_pending_review_alert(
    record_id: str,
    user_id: str,
    question: str,
    answer: str,
    regulations: list[str],
) -> None:
    webhook_url = getattr(settings, "N8N_PENDING_REVIEW_WEBHOOK_URL", None)

    if not webhook_url:
        return

    payload = {
        "record_id": record_id,
        "user_id": user_id or "N/A",
        "regulations": ", ".join(regulations) if regulations else "N/A",
        "question": question or "N/A",
        "answer": answer or "N/A",
        "status": "pending_review",
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[WARN] Failed to send pending review alert to n8n: {e}")


@router.get("/health")
def health():
    return {"status": "ok", "service": "regulatory-compliance-api"}


@router.post("/route")
def route_query(request: QueryRequest):
    framework = (request.framework or "auto").strip().lower()

    jurisdiction_hint = request.jurisdiction_hint
    regulation_hint = request.regulation_hint

    if framework == "gdpr":
        jurisdiction_hint = "EU"
        regulation_hint = "GDPR"
    elif framework == "hipaa":
        jurisdiction_hint = "US"
        regulation_hint = "HIPAA"
    elif framework == "nist":
        jurisdiction_hint = "US"
        regulation_hint = "NIST"

    regulations = []

    if regulation_hint:
        regulations = [regulation_hint.upper()]
    else:
        regulations = detect_regulations(request.question)

        if jurisdiction_hint:
            hint = jurisdiction_hint.upper()
            if hint == "EU":
                regulations = [r for r in regulations if r == "GDPR"] or ["GDPR"]
            elif hint == "US":
                regulations = [r for r in regulations if r in ["HIPAA", "NIST"]] or ["HIPAA", "NIST"]

    return {
        "question": request.question,
        "framework": framework,
        "jurisdiction_hint": jurisdiction_hint,
        "regulation_hint": regulation_hint,
        "regulations": regulations,
    }


@router.post("/query")
def query(request: QueryRequest):
    framework = (request.framework or "auto").strip().lower()

    jurisdiction_hint = request.jurisdiction_hint
    regulation_hint = request.regulation_hint

    if framework == "gdpr":
        jurisdiction_hint = "EU"
        regulation_hint = "GDPR"
    elif framework == "hipaa":
        jurisdiction_hint = "US"
        regulation_hint = "HIPAA"
    elif framework == "nist":
        jurisdiction_hint = "US"
        regulation_hint = "NIST"

    guardrail_result = evaluate_question_guardrails(request.question)

    if not guardrail_result["allowed"]:
        return {
            "question": request.question,
            "framework": framework,
            "jurisdiction_hint": jurisdiction_hint,
            "regulation_hint": regulation_hint,
            "regulations": [],
            "answer": guardrail_result["message"],
            "needs_human_review": False,
            "status": "blocked",
            "confidence": 1.0,
            "record_id": "",
            "retrieved_chunks": [],
            "reranked_chunks": [],
            "citations": "",
        }

    regulations = []

    if regulation_hint:
        regulations = [regulation_hint.upper()]
    else:
        regulations = detect_regulations(request.question)

        if jurisdiction_hint:
            hint = jurisdiction_hint.upper()
            if hint == "EU":
                regulations = [r for r in regulations if r == "GDPR"] or ["GDPR"]
            elif hint == "US":
                regulations = [r for r in regulations if r in ["HIPAA", "NIST"]] or ["HIPAA", "NIST"]

    if ENABLE_MULTI_QUERY:
        retrieved_chunks = retrieve_chunks_multi_query(request.question, regulations, top_k=8)
    else:
        retrieved_chunks = retrieve_chunks(request.question, regulations, top_k=8)

    reranked_chunks = rerank_chunks(request.question, retrieved_chunks, top_n=5)
    answer = generate_answer(request.question, reranked_chunks)

    citation_set = set()

    for item in reranked_chunks:
        metadata = item.get("metadata", {}) or {}

        citation = (
            metadata.get("citation")
            or item.get("citation")
            or metadata.get("source_label")
            or item.get("source_label")
        )

        if not citation:
            article_number = metadata.get("article_number") or item.get("article_number")
            page_number = metadata.get("page_number")
            if page_number is None:
                page_number = item.get("page_number")
            regulation = metadata.get("regulation") or item.get("regulation")

            if article_number and regulation == "GDPR":
                citation = f"GDPR {article_number}"
            elif page_number is not None and regulation:
                citation = f"{regulation} p.{page_number}"
            elif page_number is not None:
                citation = f"p.{page_number}"

        if citation:
            citation_set.add(str(citation).strip())

    citations = ", ".join(sorted(citation_set))

    source_namespaces = ", ".join(
        sorted({item.get("namespace", "") for item in reranked_chunks if item.get("namespace")})
    )

    top_confidence = calculate_confidence(reranked_chunks, citations)

    review_required = needs_human_review(
        answer,
        reranked_chunks,
        confidence=top_confidence,
    )
    status = get_review_status(review_required)

    airtable_record = log_query_result(
        record_name="Query Log",
        question=request.question,
        regulations=", ".join(regulations),
        answer=answer,
        confidence=top_confidence,
        needs_human_review=review_required,
        citations=citations,
        status=status,
        source_namespaces=source_namespaces,
        user_id=request.user_id or "",
        reviewer_notes="",
    )

    record_id = airtable_record.get("id", "") if isinstance(airtable_record, dict) else ""

    if status == "pending_review" and record_id:
        send_pending_review_alert(
            record_id=record_id,
            user_id=request.user_id or "",
            question=request.question,
            answer=answer,
            regulations=regulations,
        )

    return {
        "question": request.question,
        "framework": framework,
        "jurisdiction_hint": jurisdiction_hint,
        "regulation_hint": regulation_hint,
        "regulations": regulations,
        "answer": answer,
        "needs_human_review": review_required,
        "status": status,
        "confidence": top_confidence,
        "record_id": record_id,
        "citations": citations,
        "retrieved_chunks": retrieved_chunks,
        "reranked_chunks": reranked_chunks,
    }


@router.get("/review-result/{user_id}")
def get_review_result(user_id: str):
    record = get_latest_review_result_by_user_id(user_id)

    if not record:
        return {
            "user_id": user_id,
            "found": False,
            "message": "No review record found for this user_id.",
        }

    fields = record.get("fields", {})

    review_decision = fields.get("review_decision", "")
    original_answer = fields.get("answer", "")
    final_answer = fields.get("final_answer", "")
    reviewed_answer = fields.get("reviewed_answer", "")

    effective_final_answer = final_answer
    if not effective_final_answer:
        if review_decision == "corrected" and reviewed_answer:
            effective_final_answer = reviewed_answer
        elif review_decision == "approved" and original_answer:
            effective_final_answer = original_answer

    return {
        "user_id": user_id,
        "found": True,
        "question": fields.get("question", ""),
        "status": fields.get("status", ""),
        "review_decision": review_decision,
        "final_answer": final_answer,
        "effective_final_answer": effective_final_answer,
        "reviewed_answer": reviewed_answer,
        "reviewer_notes": fields.get("reviewer_notes", ""),
        "reviewed_by": fields.get("reviewed_by", ""),
        "reviewed_at": fields.get("reviewed_at", ""),
        "needs_human_review": fields.get("needs_human_review", False),
        "regulations": fields.get("regulations", ""),
        "citations": fields.get("citations", ""),
    }


@router.get("/review-result-record/{record_id}")
def get_review_result_by_record(record_id: str):
    record = get_review_result_by_record_id(record_id)

    if not record:
        return {
            "record_id": record_id,
            "found": False,
            "message": "No review record found for this record_id.",
        }

    fields = record.get("fields", {})

    review_decision = fields.get("review_decision", "")
    original_answer = fields.get("answer", "")
    final_answer = fields.get("final_answer", "")
    reviewed_answer = fields.get("reviewed_answer", "")

    effective_final_answer = final_answer
    if not effective_final_answer:
        if review_decision == "corrected" and reviewed_answer:
            effective_final_answer = reviewed_answer
        elif review_decision == "approved" and original_answer:
            effective_final_answer = original_answer

    return {
        "record_id": record_id,
        "found": True,
        "question": fields.get("question", ""),
        "status": fields.get("status", ""),
        "review_decision": review_decision,
        "final_answer": final_answer,
        "effective_final_answer": effective_final_answer,
        "reviewed_answer": reviewed_answer,
        "reviewer_notes": fields.get("reviewer_notes", ""),
        "reviewed_by": fields.get("reviewed_by", ""),
        "reviewed_at": fields.get("reviewed_at", ""),
        "needs_human_review": fields.get("needs_human_review", False),
        "regulations": fields.get("regulations", ""),
        "citations": fields.get("citations", ""),
    }