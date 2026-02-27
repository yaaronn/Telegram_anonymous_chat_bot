from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from app.services.match_service import find_match, leave_chat, get_partner
from app.services.moderation_service import record_message, is_banned, report_user
from app.services.analytics_service import match_created, message_sent
from app.services.analytics_service import get_stats
from app.database.db import add_report
from app.services.match_service import waiting_users
from app.database.db import get_user

router = Router()


# Chat control buttons
def chat_controls():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔁 Next", callback_data="next_chat"),
                InlineKeyboardButton(text="⛔ Stop", callback_data="stop_chat"),
                InlineKeyboardButton(text="🚩 Report", callback_data="report_user"),
            ]
        ]
    )


# Start chat
@router.message(Command("chat"))
async def find_partner(message: Message):

    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user:
        await message.answer("Please create your profile first using /profile")
        return

    if is_banned(user_id):
        await message.answer("You are banned from using this bot.")
        return

    partner = find_match(user_id)

    if partner:

        await message.bot.send_message(
            user_id,
            "🎉 Connected with someone new!\n\nSay hi 👋",
            reply_markup=chat_controls()
        )

        await message.bot.send_message(
            partner,
            "🎉 Connected with someone new!\n\nSay hi 👋",
            reply_markup=chat_controls()
        )

    else:
       await message.answer(
           f"🔎 Searching for someone...\n"
           f"People waiting: {len(waiting_users)}"
    )

# Next chat
@router.callback_query(lambda c: c.data == "next_chat")
async def next_chat(callback: CallbackQuery):

    user_id = callback.from_user.id

    partner = leave_chat(user_id)

    if partner:
        await callback.bot.send_message(
            partner,
            "Your partner left the chat."
        )

    await callback.message.answer("🔎 Finding someone new...")

    await callback.answer()

    fake_message = callback.message
    fake_message.from_user = callback.from_user

    await find_partner(fake_message)

@router.message(Command("skip"))
async def skip_chat(message: Message):

    user_id = message.from_user.id

    partner = leave_chat(user_id)

    if partner:
        await message.bot.send_message(partner, "⏭ Your partner skipped.")

    await message.answer("🔎 Finding someone new...")

    partner = find_match(user_id)

    if partner:

        await message.bot.send_message(
            user_id,
            "🎉 Connected with someone new!",
            reply_markup=chat_controls()
        )

        await message.bot.send_message(
            partner,
            "🎉 Connected with someone new!",
            reply_markup=chat_controls()
        )

    

# Stop chat
@router.callback_query(lambda c: c.data == "stop_chat")
async def stop_chat(callback: CallbackQuery):

    user_id = callback.from_user.id

    partner = leave_chat(user_id)

    if partner:
        await callback.bot.send_message(
            partner,
            "Chat ended."
        )

    await callback.message.answer("You left the chat.")

    await callback.answer()


# Report user
@router.callback_query(lambda c: c.data == "report_user")
async def report_user_handler(callback: CallbackQuery):

    user_id = callback.from_user.id
    partner = get_partner(user_id)
    await add_report(partner)
    if not partner:
        await callback.answer()
        return

    banned = report_user(partner)

    if banned:
        await callback.message.answer("User reported and banned.")
    else:
        await callback.message.answer("User reported.")

    await callback.answer()

@router.message(Command("stats"))
async def stats(message: Message):

    data = get_stats()

    await message.answer(
        f"📊 Bot Stats\n\n"
        f"Users: {data['users']}\n"
        f"Searching: {data['searching']}\n"
        f"Matches: {data['matches']}\n"
        f"Messages: {data['messages']}"
    )    

# Relay messages
@router.message()
async def relay_message(message: Message):

    if message.text and message.text.startswith("/"):
        return

    user_id = message.from_user.id

    if record_message(user_id):
        await message.answer("You are sending messages too fast.")
        return

    partner = get_partner(user_id)

    if partner:

        message_sent()
        await message.bot.copy_message(
            chat_id=partner,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )