from pydantic import BaseModel, Field


class Citation(BaseModel):
    document_id: str
    page: int | None = None
    section: str | None = None
    snippet: str


class ChatRequest(BaseModel):
    project_id: str = Field(..., description="Project scope for retrieval")
    question: str = Field(..., min_length=3)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float = Field(ge=0.0, le=1.0)
