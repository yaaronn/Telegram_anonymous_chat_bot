from aiogram import Bot, Dispatcher
from app.config import settings

from app.handlers.start import router as start_router
from app.handlers.profile import router as profile_router
from app.handlers.chat import router as chat_router

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(chat_router)
