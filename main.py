import asyncio
from bot import run_bot


if __name__ == "__main__":
    print("Бот запущен")

    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Бот остановлен")
