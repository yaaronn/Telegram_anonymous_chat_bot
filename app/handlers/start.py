from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.services.analytics_service import user_started
from app.database.db import add_user
from app.database.db import get_user

router = Router()


@router.message(Command("start"))
async def start(message: Message):

    user_id = message.from_user.id

    user = await get_user(user_id)

    # New user
    if not user:
        await message.answer(
            "👋 Welcome!\n\n"
            "Before chatting, please create your profile.\n"
            "Use /profile to begin."
        )
        return

    # Existing user
    await message.answer(
        "👋 Welcome back!\n\n"
        "Ready to meet someone new?\n\n"
        "Commands:\n"
        "💬 /chat – Start chatting\n"
        "👤 /profile – Edit profile\n"
        "📊 /stats – Bot stats"
    )