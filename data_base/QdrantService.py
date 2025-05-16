from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer


class QdrantServise:
    def __init__(self, key, url, model_name):
        self.bd = QdrantClient(api_key=key, url=url)
        self.model = SentenceTransformer(model_name)

    def search(self, query, top_k):
        hits = self.bd.query_points(
            collection_name="matstat",  # Мб потом обновим
            query=self.model.encode(query).tolist(),
            limit=top_k,
        ).points
        return hits

    def upload(self, data):
        self.bd.upload_points(
            collection_name="matstat",
            points=[
                models.PointStruct(
                    id=idx, vector=self.model.encode(doc["title"]).tolist(), payload=doc
                )
                for idx, doc in enumerate(data)
            ],
        )
        return True
