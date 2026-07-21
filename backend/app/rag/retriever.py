from __future__ import annotations

from collections.abc import Iterable

from app.models.document import DocumentChunk
from app.services.document_service import document_service


def _score_chunk(query_terms: set[str], chunk: DocumentChunk) -> tuple[int, int]:
    haystack = f"{chunk.section or ''} {chunk.title or ''} {chunk.text}".lower()
    overlap = sum(1 for term in query_terms if term in haystack)
    length_bonus = min(len(chunk.text), 2000)
    return overlap, length_bonus


class Retriever:
    async def retrieve(self, project_id: str, query: str, limit: int = 5) -> list[dict]:
        query_terms = {term for term in query.lower().split() if len(term) > 2}
        if not query_terms:
            return []

        candidate_chunks: list[DocumentChunk] = []
        if project_id and project_id != "all":
            candidate_chunks.extend(document_service.get_chunks(project_id))
        else:
            for chunks in document_service.iter_all_chunks():
                candidate_chunks.extend(chunks)

        ranked = sorted(
            candidate_chunks,
            key=lambda chunk: _score_chunk(query_terms, chunk),
            reverse=True,
        )

        results: list[dict] = []
        for chunk in ranked[:limit]:
            results.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "page": chunk.page,
                    "section": chunk.section,
                    "text": chunk.text,
                    "title": chunk.title,
                }
            )

        return results


retriever = Retriever()
