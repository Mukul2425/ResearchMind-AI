from pydantic import BaseModel


class DocumentChunk(BaseModel):
    document_id: str
    text: str
    page: int | None = None
    section: str | None = None
    title: str | None = None
