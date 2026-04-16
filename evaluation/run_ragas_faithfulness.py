import json
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.llms import llm_factory
from ragas.metrics import Faithfulness, FactualCorrectness, LLMContextRecall

INPUT_FILE = Path("evaluation/ragas_collected_samples.json")
OUTPUT_CSV = Path("evaluation/ragas_results_faithfulness_correctness_recall.csv")


def main():
    load_dotenv()

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        rows = json.load(f)

    samples = []
    for row in rows:
        samples.append(
            SingleTurnSample(
                user_input=row["user_input"],
                response=row["response"],
                retrieved_contexts=row["retrieved_contexts"],
                reference=row["reference"],
            )
        )

    dataset = EvaluationDataset(samples=samples)

    client = AsyncOpenAI()
    evaluator_llm = llm_factory("gpt-4o-mini", client=client)

    result = evaluate(
        dataset=dataset,
        metrics=[
            Faithfulness(llm=evaluator_llm),
            FactualCorrectness(llm=evaluator_llm),
            LLMContextRecall(llm=evaluator_llm),
        ],
        show_progress=True,
    )

    print("\nRAGAS result:")
    print(result)

    try:
        df = result.to_pandas()
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\nSaved row-level results to: {OUTPUT_CSV}")
        print(df.head())
    except Exception as e:
        print("\nCould not save row-level results automatically.")
        print(f"Reason: {e}")


if __name__ == "__main__":
    main()