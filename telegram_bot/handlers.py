from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async
import logging

router = Router()
logger = logging.getLogger(__name__)


class LoginForm(StatesGroup):
    email = State()
    password = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "👋 <b>Welcome to TechnoPulse Bot!</b>\n\n"
        "To connect your account, please login with your TechnoPulse credentials.\n\n"
        "Send your email:",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LoginForm.email)


@router.message(LoginForm.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(email=email)

    await message.answer(
        "📧 Email received. Now send your password:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LoginForm.password)


@router.message(LoginForm.password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()
    user_data = await state.get_data()
    email = user_data['email']

    try:
        # Проверяем логин и пароль
        from setup_django import setup_django
        setup_django()
        from django.contrib.auth import authenticate
        from django.conf import settings
        from challenges.models import User
        from django.utils import timezone

        # Аутентифицируем пользователя
        user = await sync_to_async(authenticate)(
            username=email,
            password=password
        )

        if user is not None:
            # Сохраняем Telegram данные
            user.telegram_chat_id = message.chat.id
            user.telegram_username = message.chat.username
            user.is_telegram_confirmed = True
            user.telegram_connected_at = timezone.now()
            await sync_to_async(user.save)()

            await message.answer(
                f"✅ <b>Successfully connected!</b>\n\n"
                f"Welcome, {user.name or user.email}! 🎉\n"
                f"Your TechnoPulse account is now connected to Telegram.\n\n"
                f"You'll receive notifications about:\n"
                f"• Challenge progress\n• Daily reminders\n• Achievement updates",
                parse_mode='HTML'
            )
            logger.info(f"User {user.email} connected via login form")

        else:
            await message.answer(
                "❌ <b>Invalid email or password</b>\n\n"
                "Please check your credentials and try again.\n"
                "Send /start to begin again.",
                parse_mode='HTML'
            )

    except Exception as e:
        logger.error(f"Login error: {e}")
        await message.answer(
            "❌ <b>Login failed</b>\n\n"
            "An error occurred. Please try again later.\n"
            "Send /start to begin again.",
            parse_mode='HTML'
        )

    await state.clear()


# Отмена процесса
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Login cancelled.",
        reply_markup=ReplyKeyboardRemove()
    )