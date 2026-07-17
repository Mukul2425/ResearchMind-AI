from app.models.chat import ChatRequest, ChatResponse, Citation
from app.rag.retriever import retriever


class RagService:
    async def answer_question(self, request: ChatRequest) -> ChatResponse:
        chunks = await retriever.retrieve(project_id=request.project_id, query=request.question)

        citations = [
            Citation(
                document_id=chunk.get("document_id", "unknown"),
                page=chunk.get("page"),
                section=chunk.get("section"),
                snippet=chunk.get("text", "")[:220],
            )
            for chunk in chunks
        ]

        answer = (
            "ResearchMind MVP response. Integrate your planner + LangGraph workflow here "
            "to generate grounded answers."
        )

        return ChatResponse(answer=answer, citations=citations, confidence=0.65)


rag_service = RagService()
