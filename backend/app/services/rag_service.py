from app.models.chat import ChatRequest, ChatResponse, Citation
from app.rag.retriever import retriever


class RagService:
    async def answer_question(self, request: ChatRequest) -> ChatResponse:
        chunks = await retriever.retrieve(project_id=request.project_id, query=request.question)

        if not chunks:
            return ChatResponse(
                answer=(
                    "I could not find grounded context for that question yet. "
                    "Upload a paper or broaden the project scope and try again."
                ),
                citations=[],
                confidence=0.15,
            )

        citations = [
            Citation(
                document_id=chunk.get("document_id", "unknown"),
                page=chunk.get("page"),
                section=chunk.get("section"),
                snippet=chunk.get("text", "")[:220],
            )
            for chunk in chunks
        ]

        answer_parts = [
            "Grounded answer based on the most relevant chunks:",
        ]
        for idx, chunk in enumerate(chunks[:3], start=1):
            section = chunk.get("section") or "Unknown section"
            snippet = chunk.get("text", "").strip().replace("\n", " ")[:220]
            answer_parts.append(f"{idx}. {section}: {snippet}")

        answer = "\n".join(answer_parts)
        confidence = min(0.95, 0.45 + (0.12 * len(citations)))

        return ChatResponse(answer=answer, citations=citations, confidence=confidence)


rag_service = RagService()
