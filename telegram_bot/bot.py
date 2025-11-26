import asyncio
import logging
import os
import sys
import django
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechnoProject.settings')

try:
    django.setup()
except django.core.exceptions.ImproperlyConfigured as e:
    print(f"Django setup error: {e}")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"Current directory: {os.getcwd()}")
    sys.exit(1)

load_dotenv()

from handlers import router

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()


async def main():
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")