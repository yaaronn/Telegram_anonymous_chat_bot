from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.db import update_gender, update_country


router = Router()


class ProfileSetup(StatesGroup):
    gender = State()
    preference = State()
    age = State()
    country = State()


# START PROFILE
@router.message(Command("profile"))
async def start_profile(message: Message, state: FSMContext):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨 Male", callback_data="gender_male"),
                InlineKeyboardButton(text="👩 Female", callback_data="gender_female"),
            ],
            [
                InlineKeyboardButton(text="⚧ Other", callback_data="gender_other")
            ]
        ]
    )

    await message.answer("Select your gender:", reply_markup=keyboard)
    await state.set_state(ProfileSetup.gender)


# HANDLE GENDER
@router.callback_query(ProfileSetup.gender)
async def gender_selected(callback: CallbackQuery, state: FSMContext):

    gender_map = {
        "gender_male": "Male",
        "gender_female": "Female",
        "gender_other": "Other"
    }

    gender = gender_map.get(callback.data)

    await update_gender(callback.from_user.id, gender)

    await state.update_data(gender=gender)

    pref_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨 Men", callback_data="pref_men"),
                InlineKeyboardButton(text="👩 Women", callback_data="pref_women"),
            ],
            [
                InlineKeyboardButton(text="🌍 Everyone", callback_data="pref_all")
            ]
        ]
    )

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer("Interested in:", reply_markup=pref_keyboard)

    await state.set_state(ProfileSetup.preference)

    await callback.answer()


# HANDLE PREFERENCE
@router.callback_query(ProfileSetup.preference)
async def preference_selected(callback: CallbackQuery, state: FSMContext):

    pref_map = {
        "pref_men": "Male",
        "pref_women": "Female",
        "pref_all": "Everyone"
    }

    preference = pref_map.get(callback.data)

    await state.update_data(preference=preference)

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer("Enter your age:")

    await state.set_state(ProfileSetup.age)

    await callback.answer()


# HANDLE AGE
@router.message(ProfileSetup.age)
async def get_age(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Please enter a valid age.")
        return

    age = int(message.text)

    if age < 18 or age > 100:
        await message.answer("Age must be between 18 and 100.")
        return

    await state.update_data(age=age)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇮🇳 India", callback_data="country_india"),
                InlineKeyboardButton(text="🇺🇸 USA", callback_data="country_usa"),
            ],
            [
                InlineKeyboardButton(text="🇬🇧 UK", callback_data="country_uk"),
                InlineKeyboardButton(text="🌍 Other", callback_data="country_other"),
            ]
        ]
    )

    await message.answer("Select your country:", reply_markup=keyboard)

    await state.set_state(ProfileSetup.country)


# HANDLE COUNTRY
@router.callback_query(ProfileSetup.country)
async def country_selected(callback: CallbackQuery, state: FSMContext):

    country_map = {
        "country_india": "India",
        "country_usa": "USA",
        "country_uk": "UK",
        "country_other": "Other"
    }

    country = country_map.get(callback.data)

    await update_country(callback.from_user.id, country)

    await state.update_data(country=country)

    data = await state.get_data()

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        f"✅ Profile Saved!\n\n"
        f"Name: {callback.from_user.first_name}\n"
        f"Gender: {data['gender']}\n"
        f"Interested in: {data['preference']}\n"
        f"Age: {data['age']}\n"
        f"Country: {data['country']}"
    )

    await state.clear()

    await callback.answer()