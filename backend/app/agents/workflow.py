from dataclasses import dataclass


@dataclass
class AgentResult:
    answer: str
    citations: list[dict]
    confidence: float


class ResearchAgentWorkflow:
    async def run(self, question: str, context_chunks: list[dict]) -> AgentResult:
        # Placeholder for LangGraph planner -> analyst -> citation -> critic flow.
        return AgentResult(
            answer=f"Agentic response placeholder for: {question}",
            citations=context_chunks,
            confidence=0.7,
        )


workflow = ResearchAgentWorkflow()
