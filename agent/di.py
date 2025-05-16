from .agent import Agent, RAG
from .llm_client import GigaLLM
from .retriever import Retriever
from .gateway import QdrantGateway


def get_agent() -> Agent:
    chat = GigaLLM()
    db = QdrantGateway()
    retriever = Retriever(db)
    rag = RAG(retriever, chat)

    return rag
