import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
debug = bool(os.getenv("DEBUG"))


@dataclass
class BotConfig:
    BOT_TOKEN: str = os.getenv("TOKEN") if not debug else os.getenv("TEST_TOKEN")


@dataclass
class AgentConfig:
    llm_api_key: Optional[str] = os.getenv("LLM_API_KEY")
    model: str = "giga_chat"
    temperature: float = 0.1
    max_tokens: Optional[int] = 4096

    qdrant_url: Optional[str] = os.getenv("QDRANT_URL")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    embedder_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    top_k: int = 3
    similarity_threshold: float = 0.7
