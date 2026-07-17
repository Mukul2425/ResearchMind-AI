class Retriever:
    async def retrieve(self, project_id: str, query: str) -> list[dict]:
        # Placeholder retrieval result. Replace with Qdrant search + rerank.
        return [
            {
                "document_id": f"{project_id}-doc-1",
                "page": 1,
                "section": "Abstract",
                "text": f"Relevant chunk for query: {query}",
            }
        ]


retriever = Retriever()
