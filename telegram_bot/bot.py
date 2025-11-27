# bot.py
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage  # ← Добавь это
from dotenv import load_dotenv

# Настраиваем Django
from telegram_bot.setup_django import setup_django

setup_django()

from telegram_bot.handlers import router

load_dotenv()

async def send_message_async(chat_id, text):
    print("send_message")
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    await bot.send_message(chat_id, text)

async def main():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    storage = MemoryStorage()  # ← Хранилище для состояний
    dp = Dispatcher(storage=storage)  # ← Передаем хранилище

    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Bot started polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())