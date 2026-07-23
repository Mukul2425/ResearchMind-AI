from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
except ImportError:  # pragma: no cover - optional local dependency
    QdrantClient = None
    qmodels = None

from app.models.document import DocumentChunk
from app.utils.config import settings


@dataclass(frozen=True)
class StoredVectorChunk:
    chunk: DocumentChunk
    vector: list[float]
    payload: dict[str, Any]


class VectorStore:
    def __init__(self) -> None:
        self.collection_name = settings.qdrant_collection
        self.dimension = settings.embedding_dimension
        self._memory_index: dict[str, StoredVectorChunk] = {}
        self._client = self._build_client()
        self._ensure_collection()

    def _build_client(self) -> QdrantClient | None:
        if QdrantClient is None:
            return None

        try:
            return QdrantClient(url=settings.qdrant_url)
        except Exception:
            return None

    def _ensure_collection(self) -> None:
        if self._client is None:
            return

        if qmodels is None:
            self._client = None
            return

        try:
            collections = self._client.get_collections().collections
            existing_names = {collection.name for collection in collections}
            if self.collection_name in existing_names:
                return

            self._client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self.dimension,
                    distance=qmodels.Distance.COSINE,
                ),
            )
        except Exception:
            self._client = None

    def _tokenize(self, text: str) -> list[str]:
        return [token for token in text.lower().split() if token]

    def embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for token in self._tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % self.dimension
            weight = 1.0 + (sum(digest[4:8]) / 1024.0)
            vector[index] += weight

        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]
        return vector

    def index_chunks(self, chunks: list[DocumentChunk]) -> None:
        if not chunks:
            return

        if qmodels is None:
            return

        points: list[qmodels.PointStruct] = []
        for chunk in chunks:
            combined_text = f"{chunk.section or ''} {chunk.title or ''} {chunk.text}".strip()
            vector = self.embed_text(combined_text)
            payload = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "page": chunk.page,
                "page_end": chunk.page_end,
                "section": chunk.section,
                "title": chunk.title,
                "text": chunk.text,
                "authors": chunk.authors,
            }
            stored = StoredVectorChunk(chunk=chunk, vector=vector, payload=payload)
            self._memory_index[chunk.chunk_id] = stored
            points.append(
                qmodels.PointStruct(
                    id=chunk.chunk_id,
                    vector=vector,
                    payload=payload,
                )
            )

        if self._client is None:
            return

        try:
            self._client.upsert(collection_name=self.collection_name, points=points)
        except Exception:
            self._client = None

    def search(self, query: str, limit: int = 5, document_id: str | None = None) -> list[dict[str, Any]]:
        query_vector = self.embed_text(query)
        if not query_vector:
            return []

        if self._client is not None and qmodels is not None:
            try:
                query_filter = None
                if document_id and document_id != "all":
                    query_filter = qmodels.Filter(
                        must=[
                            qmodels.FieldCondition(
                                key="document_id",
                                match=qmodels.MatchValue(value=document_id),
                            )
                        ]
                    )

                results = self._client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=limit,
                    query_filter=query_filter,
                )
                return [self._point_to_result(point) for point in results]
            except Exception:
                self._client = None

        return self._memory_search(query_vector=query_vector, limit=limit, document_id=document_id)

    def _memory_search(self, query_vector: list[float], limit: int, document_id: str | None) -> list[dict[str, Any]]:
        scored: list[tuple[float, StoredVectorChunk]] = []
        for stored in self._memory_index.values():
            if document_id and document_id != "all" and stored.chunk.document_id != document_id:
                continue
            score = self._cosine_similarity(query_vector, stored.vector)
            scored.append((score, stored))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [self._stored_to_result(stored, score) for score, stored in scored[:limit]]

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        return sum(a * b for a, b in zip(left, right))

    def _point_to_result(self, point: Any) -> dict[str, Any]:
        payload = point.payload or {}
        return {
            "chunk_id": str(point.id),
            "score": float(point.score or 0.0),
            "document_id": payload.get("document_id", "unknown"),
            "page": payload.get("page"),
            "page_end": payload.get("page_end"),
            "section": payload.get("section"),
            "title": payload.get("title"),
            "text": payload.get("text", ""),
        }

    def _stored_to_result(self, stored: StoredVectorChunk, score: float) -> dict[str, Any]:
        payload = stored.payload
        return {
            "chunk_id": payload.get("chunk_id", stored.chunk.chunk_id),
            "score": score,
            "document_id": payload.get("document_id", stored.chunk.document_id),
            "page": payload.get("page", stored.chunk.page),
            "page_end": payload.get("page_end", stored.chunk.page_end),
            "section": payload.get("section", stored.chunk.section),
            "title": payload.get("title", stored.chunk.title),
            "text": payload.get("text", stored.chunk.text),
        }


vector_store = VectorStore()
