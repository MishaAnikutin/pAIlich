from dataclasses import dataclass
from typing import List

from config import AgentConfig

from qdrant_client import QdrantClient, models
from qdrant_client.conversions.common_types import ScoredPoint
from sentence_transformers import SentenceTransformer


@dataclass
class BootData:
    title: str
    text: str


class Subjects:
    matstat: str = "matstat"


class QdrantGateway:

    def __init__(self):
        self._client = QdrantClient(
            api_key=AgentConfig.qdrant_api_key, url=AgentConfig.qdrant_url
        )
        self._embedder = SentenceTransformer(AgentConfig.embedder_name)

    def search(
        self, query: str, top_k: int, collection_name: Subjects = Subjects.matstat
    ) -> List[ScoredPoint]:
        embeddings = self._embedder.encode(query).tolist()

        return self._client.query_points(
            collection_name=collection_name,
            query=embeddings,
            limit=top_k,
        ).points

    def upload(
        self, data: List[BootData], collection_name: Subjects = Subjects.matstat
    ) -> None:
        points = (
            [
                models.PointStruct(
                    id=idx,
                    vector=self._embedder.encode(doc["title"]).tolist(),
                    payload=doc,
                )
                for idx, doc in enumerate(data)
            ],
        )

        self._client.upload_points(collection_name=collection_name, points=points)
