from agent import *
from gateway import *
from retriever import *
from function import *
import markdown
from llm_client import Gigaclass
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import *

# Инициализация компонентов
chat = Gigaclass()
db = QdrantGateway()
ret = Retriever(db, 'None')
rag = RAG(ret, chat)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне сообщение — я отвечу тебе по конспектам Палыча")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = rag.get_answer(user_message) 
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации ответа: {e}")

def main():
    TOKEN = Config.bot_token
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()



