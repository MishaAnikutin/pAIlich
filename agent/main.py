from dataclasses import dataclass
from typing import Optional

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek


SYSTEM_PROMPT = """Ты полезный ассистент по математической статистике в ВУЗе РАНХиГС в институте ЭМИТ на отделении
экономики. Твоя задача отвечать на вопросы по математической статистике на основе введенных вопросов по полученному контексту

Отвечай строго по контексту, если он релевантный. Это вырезки из учебника, и очень важно следовать им слово в слово. 
Если по твоему мнению информация из контекста не релевантна, то попроси пользователя уточнить вопрос.
"""


@dataclass
class Config:
    model: str = "deepseek-chat"
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None
    top_k: int = 3
    similarity_threshold: float = 0.7


class Retriever:
    def __init__(self):
        self.top_k = Config.top_k
        self.similarity_threshold = Config.similarity_threshold

    def retrieve(self, query: str) -> str:
        ...


class DeepSeekClient:
    def __init__(self):
        self.llm = ChatDeepSeek(
            model=Config.model,
            temperature=Config.temperature,
            max_tokens=Config.max_tokens,
            api_key=Config.api_key
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Контекст:\n{context}\n\nВопрос пользователя: {query}")
        ])

    def generate(self, context: str, query: str) -> str:
        prompt = self.prompt_template.format(context=context, query=query)
        response = self.llm.invoke(prompt)
        return response.content


class RAGPipeline:
    def __init__(self, retriever: Retriever, llm_client: DeepSeekClient):
        self.chain = RunnablePassthrough.assign(
            context=lambda x: retriever.retrieve(x["query"])
        ) | {
            "context": lambda x: x["context"],
            "query": lambda x: x["query"]
        } | (lambda x: llm_client.generate(x["context"], x["query"]))

    def run(self, query: str) -> str:
        return self.chain.invoke({"query": query})


class AssistantService:
    def __init__(self):
        self.retriever = Retriever()
        self.llm_client = DeepSeekClient()
        self.pipeline = RAGPipeline(self.retriever, self.llm_client)

    def get_answer(self, query: str) -> str:
        return self.pipeline.run(query)


if __name__ == "__main__":
    config = Config(
        model="deepseek-chat",
        temperature=0.3,
        top_k=5,
        similarity_threshold=0.8
    )

    assistant = AssistantService()
    response = assistant.get_answer("Что такое распределение Хи квадрат?")
    print(f"Assistant Response:\n{response}")
