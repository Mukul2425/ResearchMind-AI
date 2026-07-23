from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvalCase:
    name: str
    query: str
    project_id: str = "all"
    expected_terms: tuple[str, ...] = ()
    expected_sections: tuple[str, ...] = ()
    expected_document_ids: tuple[str, ...] = ()


def _load_cases(path: Path) -> list[EvalCase]:
    raw_cases = json.loads(path.read_text(encoding="utf-8"))
    cases: list[EvalCase] = []
    for raw_case in raw_cases:
        cases.append(
            EvalCase(
                name=raw_case["name"],
                query=raw_case["query"],
                project_id=raw_case.get("project_id", "all"),
                expected_terms=tuple(raw_case.get("expected_terms", [])),
                expected_sections=tuple(raw_case.get("expected_sections", [])),
                expected_document_ids=tuple(raw_case.get("expected_document_ids", [])),
            )
        )
    return cases


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _metric_hit(expected_values: tuple[str, ...], actual_value: str | None) -> bool:
    if not expected_values:
        return True
    if not actual_value:
        return False
    normalized_actual = _normalize(actual_value)
    return any(expected.lower() in normalized_actual for expected in expected_values)


def _get_retriever():
    from app.rag.retriever import retriever

    return retriever


async def evaluate_case(case: EvalCase, limit: int = 5) -> dict[str, Any]:
    retriever = _get_retriever()
    results = await retriever.retrieve(project_id=case.project_id, query=case.query, limit=limit)

    top_result = results[0] if results else None
    top_section = top_result.get("section") if top_result else None
    top_document_id = top_result.get("document_id") if top_result else None
    top_text = top_result.get("text", "") if top_result else ""

    section_hit = _metric_hit(case.expected_sections, top_section)
    document_hit = _metric_hit(case.expected_document_ids, top_document_id)
    term_hit = True
    if case.expected_terms:
        normalized_text = _normalize(top_text)
        term_hit = any(term.lower() in normalized_text for term in case.expected_terms)

    top1_hit = section_hit and document_hit and term_hit
    reciprocal_rank = 0.0
    for index, result in enumerate(results, start=1):
        section_match = _metric_hit(case.expected_sections, result.get("section"))
        document_match = _metric_hit(case.expected_document_ids, result.get("document_id"))
        text_match = True
        if case.expected_terms:
            normalized_text = _normalize(result.get("text", ""))
            text_match = any(term.lower() in normalized_text for term in case.expected_terms)

        if section_match and document_match and text_match:
            reciprocal_rank = 1.0 / index
            break

    return {
        "name": case.name,
        "query": case.query,
        "top1_hit": top1_hit,
        "mrr": reciprocal_rank,
        "top_result": top_result,
        "results": results,
    }


async def evaluate_cases(cases: list[EvalCase], limit: int = 5) -> dict[str, Any]:
    if not cases:
        return {
            "case_count": 0,
            "top1_accuracy": 0.0,
            "mean_reciprocal_rank": 0.0,
            "cases": [],
        }

    detailed_results = [await evaluate_case(case, limit=limit) for case in cases]
    case_count = len(detailed_results)
    top1_accuracy = sum(1 for result in detailed_results if result["top1_hit"]) / case_count
    mean_reciprocal_rank = sum(result["mrr"] for result in detailed_results) / case_count

    return {
        "case_count": case_count,
        "top1_accuracy": round(top1_accuracy, 3),
        "mean_reciprocal_rank": round(mean_reciprocal_rank, 3),
        "cases": detailed_results,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate retrieval ranking quality")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "eval_cases.example.json",
        help="Path to a JSON file containing evaluation cases",
    )
    parser.add_argument("--limit", type=int, default=5, help="Number of results to inspect per query")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    cases = _load_cases(args.cases)
    import asyncio

    results = asyncio.run(evaluate_cases(cases, limit=args.limit))
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
