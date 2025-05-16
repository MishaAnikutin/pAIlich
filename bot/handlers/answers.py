from aiogram import Router, types
from aiogram.filters import Command

from bot.service import AgentService, GreetingService

answers_router = Router()
answers_service = AgentService()
greeting_service = GreetingService()


@answers_router.message(Command("start"))
async def start_handler(message: types.Message):
    greet = await greeting_service.greet(username=message.chat.username)
    await message.answer(greet)


@answers_router.message()
async def answering_handler(message: types.Message):
    thinking_message = await message.answer(text="<i>Бот думает...</i>")

    answer = answers_service.get_answer(query=message.text)

    await thinking_message.delete()
    await message.answer(answer)
