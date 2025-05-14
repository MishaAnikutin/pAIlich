from config import Config
from gateway import QdrantGateway


class Retriever:
    def __init__(self, gateway: QdrantGateway, embedder):
        self.gateway = gateway
        self.embedder = embedder

        self.top_k = Config.top_k
        self.similarity_threshold = Config.similarity_threshold

    def retrieve(self, query: str) -> str:
        """Отбирает первые top_k чанков с близостью не меньше similarity_threshold"""

        relevant_chunks = self.gateway.search(query=query, top_k=self.top_k)

        total_answer = [
            chunk.payload['text']
            for chunk in relevant_chunks
            if chunk.score > self.similarity_threshold
        ] # Тут смотреть gateway

        return "".join(
            [f"- {i + 1}) {text}\n\n" for i, text in enumerate(total_answer)]
        )
