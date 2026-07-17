from uuid import uuid4

from fastapi import UploadFile

from app.parsers.pdf_parser import parse_pdf


class DocumentService:
    async def ingest_pdf(self, file: UploadFile) -> str:
        # Placeholder: replace with S3/Supabase storage + parser/chunker pipeline.
        raw_bytes = await file.read()
        _ = parse_pdf(raw_bytes)
        return str(uuid4())


document_service = DocumentService()
