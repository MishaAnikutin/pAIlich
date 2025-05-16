from jinja2 import Environment, FileSystemLoader


class GreetingService:
    def __init__(self):
        self._env = Environment(
            loader=FileSystemLoader("bot/templates/"), enable_async=True
        )
        self._template = self._env.get_template("greeting.jinja")

    async def greet(self, username):
        return await self._template.render_async(username=username)
