from uuid import uuid4

from fastapi import UploadFile

from app.models.document import DocumentChunk
from app.parsers.pdf_parser import parse_pdf
from app.rag.chunker import chunk_document


class DocumentService:
    def __init__(self) -> None:
        self._parsed_by_document: dict[str, dict] = {}
        self._chunks_by_document: dict[str, list[DocumentChunk]] = {}

    async def ingest_pdf(self, file: UploadFile) -> str:
        raw_bytes = await file.read()
        document_id = str(uuid4())

        parsed_document = parse_pdf(raw_bytes)
        chunks = chunk_document(document_id=document_id, parsed_document=parsed_document)

        self._parsed_by_document[document_id] = parsed_document
        self._chunks_by_document[document_id] = chunks
        return document_id

    def get_chunks(self, document_id: str) -> list[DocumentChunk]:
        return self._chunks_by_document.get(document_id, [])


document_service = DocumentService()
