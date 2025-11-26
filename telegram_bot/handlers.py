from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from asgiref.sync import sync_to_async

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    if len(message.text.split()) > 1:
        token = message.text.split()[1]
        await connect_telegram_account(message, token)

    else:
        await message.answer(
            "👋 <b>Welcome to TechnoPulse Bot!</b>\n\n"
            "To connect your account:\n"
            "1. Open TechnoPulse app\n" 
            "2. Go to Settings → Telegram Connection\n"
            "3. Generate and use the connection link\n\n"
            "Need help? Send /help",
            parse_mode='HTML'
        )

async def connect_telegram_account(message: Message, token):
    try:
        from setup_django import setup_django
        setup_django()
        from django.utils import timezone
        import jwt
        from django.conf import settings
        from challenges.models import User
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['id']
        user = await sync_to_async(User.objects.get)(id=user_id)
        user.telegram_chat_id = message.chat.id
        user.telegram_username = message.chat.username
        user.is_telegram_connected = True
        user.telegram_connected_at = timezone.now()
        await sync_to_async(user.save)()

        await message.answer("You successfully connected your telegram account.")
    except jwt.ExpiredSignatureError:
        await message.answer("Unfortunately, your link expired")
    except (jwt.InvalidTokenError, User.DoesNotExist):
        await message.answer("Incorrect link was given.")