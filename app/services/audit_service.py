from airtable import Airtable
from app.core.config import settings


def get_airtable_client():
    return Airtable(
        settings.AIRTABLE_BASE_ID,
        settings.AIRTABLE_TABLE_NAME,
        settings.AIRTABLE_API_KEY,
    )


def log_query_result(
    record_name: str,
    question: str,
    regulations: str,
    answer: str,
    confidence: float | None = None,
    needs_human_review: bool = False,
    citations: str = "",
    status: str = "generated",
    source_namespaces: str = "",
    user_id: str = "",
    reviewer_notes: str = "",
):
    airtable = get_airtable_client()

    fields = {
        "record_name": record_name,
        "question": question,
        "regulations": regulations,
        "answer": answer,
        "needs_human_review": needs_human_review,
        "citations": citations,
        "status": status,
        "source_namespaces": source_namespaces,
        "user_id": user_id,
        "reviewer_notes": reviewer_notes,
    }

    if confidence is not None:
        fields["confidence"] = confidence

    if status == "pending_review":
        fields["review_decision"] = "pending"

    return airtable.insert(fields)


def get_latest_review_result_by_user_id(user_id: str):
    airtable = get_airtable_client()

    if not user_id:
        return None

    records = airtable.get_all(
        formula=f"{{user_id}}='{user_id}'",
        sort=[("created_at", "desc")]
    )

    if not records:
        return None

    return records[0]


def get_review_result_by_record_id(record_id: str):
    airtable = get_airtable_client()

    if not record_id:
        return None

    try:
        return airtable.get(record_id)
    except Exception:
        return None