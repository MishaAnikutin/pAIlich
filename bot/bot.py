from aiogram import Bot, Dispatcher

from config import BotConfig
from .handlers import answers_router


async def run_bot() -> None:
    bot = Bot(token=BotConfig.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(answers_router)

    await dp.start_polling(bot)
