from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

from config import Config

SYSTEM_PROMPT = """
Ты полезный ассистент по математической статистике в ВУЗе РАНХиГС в институте ЭМИТ на отделении
экономики. Твоя задача отвечать на вопросы по математической статистике на основе введенных 
вопросов по полученному контексту

Отвечай строго по контексту, если он релевантный. Это вырезки из учебника, и очень важно следовать им слово в слово. 
Если по твоему мнению информация из контекста не релевантна, то попроси пользователя уточнить вопрос.
"""


class DeepSeekClient:
    def __init__(self):
        self.llm = ChatDeepSeek(
            model=Config.model,
            temperature=Config.temperature,
            max_tokens=Config.max_tokens,
            api_key=Config.llm_api_key,
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("human", "Контекст:\n{context}\n\nВопрос пользователя: {query}"),
            ]
        )

    def generate(self, context: str, query: str) -> str:
        prompt = self.prompt_template.format(context=context, query=query)
        response = self.llm.invoke(prompt)
        return response.content
