from __future__ import annotations

from typing import Any


class RetrievalReranker:
    def _tokenize(self, text: str) -> set[str]:
        return {token for token in text.lower().split() if len(token) > 2}

    def rerank(self, query: str, results: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
        if not results:
            return []

        query_terms = self._tokenize(query)
        if not query_terms:
            return results[:limit]

        scored_results: list[tuple[float, dict[str, Any]]] = []
        for result in results:
            text = f"{result.get('section', '')} {result.get('title', '')} {result.get('text', '')}".lower()
            text_terms = self._tokenize(text)
            overlap = len(query_terms & text_terms)
            section_boost = 0.0
            section = (result.get("section") or "").lower()
            if any(term in section for term in query_terms):
                section_boost = 0.15

            vector_score = float(result.get("score", 0.0))
            lexical_score = overlap / max(len(query_terms), 1)
            combined_score = (vector_score * 0.7) + (lexical_score * 0.25) + section_boost

            reranked = dict(result)
            reranked["rerank_score"] = round(combined_score, 4)
            scored_results.append((combined_score, reranked))

        scored_results.sort(key=lambda item: item[0], reverse=True)
        return [result for _, result in scored_results[:limit]]


reranker = RetrievalReranker()
