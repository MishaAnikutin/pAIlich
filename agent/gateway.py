from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from config import Config


class Subjects:
    matstat: str = "matstat"


class QdrantGateway:

    # FIXME: нарушение SRP, нужно их не инициализировать а задавать. Но можно забить
    def __init__(self):
        self.bd = QdrantClient(api_key=Config.qdrant_api_key, url=Config.qdrant_url)
        self.embedder = SentenceTransformer(Config.embedder_name)

    def search(self, query, top_k, collection_name: Subjects = Subjects.matstat):
        embeddings = self.embedder.encode(query).tolist()

        return self.bd.query_points(
            collection_name=collection_name,
            query=embeddings,
            limit=top_k,
        ).points

    # TODO: Какие типы у data ?
    def upload(self, data, collection_name: Subjects = Subjects.matstat):
        points = (
            [
                models.PointStruct(
                    id=idx,
                    vector=self.embedder.encode(
                        doc["title"]
                    ).tolist(),  # TODO: Какая схема у doc ?
                    payload=doc,
                )
                for idx, doc in enumerate(data)
            ],
        )

        self.bd.upload_points(collection_name=collection_name, points=points)
        # FIXME: почему всегда возвращает True?
        return True
