import json
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:8000/query"
INPUT_FILE = Path("evaluation/datasets/ragas_pilot_questions.json")
OUTPUT_FILE = Path("evaluation/ragas_collected_samples.json")


def extract_retrieved_contexts(api_data: dict) -> list[str]:
    contexts = []

    for chunk in api_data.get("retrieved_chunks", []):
        text = ""

        if isinstance(chunk, dict):
            text = str(chunk.get("text", "")).strip()

            if not text:
                metadata = chunk.get("metadata", {})
                if isinstance(metadata, dict):
                    text = str(metadata.get("text", "")).strip()

        if text:
            contexts.append(text)

    return contexts


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        questions = json.load(f)

    collected_rows = []

    for i, item in enumerate(questions, start=1):
        user_input = item["user_input"]
        reference = item["reference"]
        framework = item["framework"]

        print(f"[{i}/{len(questions)}] Running: {user_input}")

        response = requests.post(
            API_URL,
            json={
                "question": user_input,
                "user_id": "ragas_eval_user",
                "framework": framework,
            },
            timeout=120,
        )
        response.raise_for_status()
        api_data = response.json()

        row = {
            "user_input": user_input,
            "reference": reference,
            "framework": framework,
            "response": api_data.get("answer", ""),
            "retrieved_contexts": extract_retrieved_contexts(api_data),
            "confidence": api_data.get("confidence"),
            "status": api_data.get("status"),
            "record_id": api_data.get("record_id"),
            "citations": api_data.get("citations"),
        }

        collected_rows.append(row)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(collected_rows, f, indent=2, ensure_ascii=False)

    print(f"\nSaved collected samples to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()