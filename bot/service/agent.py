from agent import get_agent


class AgentService:
    def __init__(self):
        self._agent = get_agent()

    def get_answer(self, query: str) -> str:
        return self._agent.get_answer(query)
