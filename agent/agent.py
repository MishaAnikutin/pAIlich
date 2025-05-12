from abc import ABC, abstractmethod
from langchain_core.runnables import RunnablePassthrough

from retriever import Retriever
from llm_client import DeepSeekClient


class Agent(ABC):
    @abstractmethod
    def get_answer(self, query: str) -> str: ...


class RAG(Agent):
    def __init__(self, retriever: Retriever, llm_client: DeepSeekClient):
        self.retriever = retriever
        self.llm_client = llm_client

        self.chain = (
            RunnablePassthrough.assign(context=lambda x: retriever.retrieve(x["query"]))
            | {"context": lambda x: x["context"], "query": lambda x: x["query"]}
            | (lambda x: llm_client.generate(x["context"], x["query"]))
        )

    def get_answer(self, query: str) -> str:
        return self.chain.invoke({"query": query})
