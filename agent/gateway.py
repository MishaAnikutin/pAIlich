from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from config import Config
from typing import List, TypedDict,Optional,Dict


class BootData(TypedDict):
    title:str
    text:str

class ScoredPoint(TypedDict):
    id: int
    version: int
    score: float
    payload: Dict[str, str]
    vector: Optional[List[float]]
    shard_key: Optional[str]
    order_value: Optional[float]


class Subjects:
    matstat: str = "matstat"




class QdrantGateway:

    # FIXME: нарушение SRP, нужно их не инициализировать а задавать. Но можно забить
    def __init__(self):
        self.bd = QdrantClient(api_key=Config.qdrant_api_key, url=Config.qdrant_url)
        self.embedder = SentenceTransformer(Config.embedder_name)

    def search(self, query:str, top_k:int, collection_name: Subjects = Subjects.matstat) -> List[ScoredPoint]:
        embeddings = self.embedder.encode(query).tolist()

        return self.bd.query_points(
            collection_name=collection_name,
            query=embeddings,
            limit=top_k,
        ).points

    def upload(self, data: List[BootData], collection_name: Subjects = Subjects.matstat) -> None:
        points = (
            [
                models.PointStruct(
                    id=idx,
                    vector=self.embedder.encode(
                        doc["title"]
                    ).tolist(),
                    payload=doc,
                )
                for idx, doc in enumerate(data)
            ],
        )

        self.bd.upload_points(collection_name=collection_name, points=points)
        # FIXME: почему всегда возвращает True? А что?
        return None
