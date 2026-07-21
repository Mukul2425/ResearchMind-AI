from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    page: int | None = None
    page_end: int | None = None
    section: str | None = None
    title: str | None = None
    authors: list[str] = Field(default_factory=list)
