from config import AgentConfig
from .gateway import QdrantGateway, ScoredPoint


class Retriever:
    def __init__(self, gateway: QdrantGateway):
        self.gateway = gateway

        self.top_k = AgentConfig.top_k
        self.similarity_threshold = AgentConfig.similarity_threshold

    def retrieve(self, query: str) -> str:
        """Отбирает первые top_k чанков с близостью не меньше similarity_threshold"""
        relevant_chunks: list[ScoredPoint] = self.gateway.search(
            query=query, top_k=self.top_k
        )

        total_answer = [
            chunk.payload["text"]
            for chunk in relevant_chunks
            if chunk.score > self.similarity_threshold
        ]

        return "".join(
            [f"- {i + 1}) {text}\n\n" for i, text in enumerate(total_answer)]
        )
