from fastapi import APIRouter, Query

from app.rag.retriever import retriever
from app.services.document_service import document_service

router = APIRouter()


@router.get("/documents/{document_id}")
async def get_document_debug(document_id: str) -> dict:
    parsed_document = document_service.get_parsed_document(document_id)
    chunks = document_service.get_chunks(document_id)

    return {
        "document_id": document_id,
        "parsed_document": parsed_document,
        "chunks": [chunk.model_dump() for chunk in chunks],
        "chunk_count": len(chunks),
    }


@router.get("/search")
async def debug_search(
    query: str = Query(..., min_length=3),
    document_id: str = Query("all"),
    limit: int = Query(5, ge=1, le=10),
) -> dict:
    results = await retriever.retrieve(project_id=document_id, query=query, limit=limit)
    return {
        "query": query,
        "document_id": document_id,
        "limit": limit,
        "results": results,
    }