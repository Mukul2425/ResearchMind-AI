from fastapi import APIRouter, File, UploadFile

from app.services.document_service import document_service

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, str]:
    document_id = await document_service.ingest_pdf(file)
    return {"document_id": document_id, "filename": file.filename or "unknown"}
