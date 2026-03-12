from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from app.config import settings

router = Router(name="onboarding")


class OnboardingStates(StatesGroup):
    choose_language = State()
    confirm_adult = State()


LANGUAGE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang:en")],
        [InlineKeyboardButton(text="हिंदी", callback_data="lang:hi")],
    ]
)


def adult_confirmation_kb(lang: str) -> InlineKeyboardMarkup:
    text = "I am 18+" if lang == "en" else "मेरी आयु 18+ है"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data="adult:yes")]])


def webapp_kb(lang: str) -> ReplyKeyboardMarkup:
    button_text = "Open Web App" if lang == "en" else "वेब ऐप खोलें"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text, web_app=WebAppInfo(url=settings.webapp_url))]],
        resize_keyboard=True,
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(OnboardingStates.choose_language)
    await message.answer("Choose your language / भाषा चुनें", reply_markup=LANGUAGE_KB)


@router.callback_query(OnboardingStates.choose_language, F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.split(":", maxsplit=1)[1]
    await state.update_data(language=lang)
    await state.set_state(OnboardingStates.confirm_adult)
    prompt = "Please confirm you are 18+" if lang == "en" else "कृपया पुष्टि करें कि आपकी आयु 18+ है"
    await callback.message.answer(prompt, reply_markup=adult_confirmation_kb(lang))
    await callback.answer()


@router.callback_query(OnboardingStates.confirm_adult, F.data == "adult:yes")
async def confirm_adult(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    done = "Onboarding completed. Open the app below." if lang == "en" else "ऑनबोर्डिंग पूरी हुई। नीचे ऐप खोलें।"
    await state.clear()
    await callback.message.answer(done, reply_markup=webapp_kb(lang))
    await callback.answer()
