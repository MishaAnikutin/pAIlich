import os
import dotenv
from typing import Optional
from dataclasses import dataclass


dotenv.load_dotenv()


@dataclass
class Config:
    llm_api_key: Optional[str] = os.getenv("LLM_API_KEY")
    model: str = "giga_chat"
    temperature: float = 0.1
    max_tokens: Optional[int] = 4096

    qdrant_url: Optional[str] = os.getenv("QDRANT_URL")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    embedder_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    top_k: int = 3
    similarity_threshold: float = 0.7

    bot_token:str = os.getenv('TOKEN')