def format_output(question: str, llm_result: dict, regulations: list[str], response_time: float):
    final_answer = llm_result.get("final_answer", "")
    recommended_action = llm_result.get("recommended_action", "")
    risk_note = llm_result.get("risk_note", "")
    citations = llm_result.get("citations", [])
    confidence = llm_result.get("confidence", 0.0)

    answer_text = f"""Question:
{question}

Answer:
{final_answer}

Recommended action:
{recommended_action}

Risk note:
{risk_note}

Citations:
{", ".join(citations)}

Confidence:
{confidence}

Regulations:
{" + ".join(regulations)}

Response time:
{round(response_time, 2)} seconds
"""
    return {
        "question": question,
        "answer": final_answer,
        "recommended_action": recommended_action,
        "risk_note": risk_note,
        "citations": citations,
        "confidence": confidence,
        "regulations": regulations,
        "response_time_seconds": round(response_time, 2),
        "formatted_text": answer_text,
    }