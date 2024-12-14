import uuid
import random
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart

from keyboards import keyboards
from config_data.config import Config, load_config
from database import database

from GigaQueryEngine import create_random_text, prompts_text

from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    waiting_for_query = State()


user_router = Router()
config: Config = load_config()


async def send_text(callback_or_message, state: FSMContext, theme_text=None, is_query=False, template_text="Результат запроса:\n"):
    send_method = callback_or_message.message.answer if isinstance(callback_or_message,
                                                                   CallbackQuery) else callback_or_message.answer
    tg_id = callback_or_message.from_user.id if isinstance(callback_or_message,
                                                           CallbackQuery) else callback_or_message.from_user.id

    try:
        await database.process_user_query(tg_id)
    except Exception:
        await send_method(text='У вас закончились бесплатные запросы! Для продолжения необходимо купить подписку!',
                          reply_markup=keyboards.buy_sub())
        return

    story = create_random_text(theme_text, is_query)
    print(theme_text)
    await state.update_data(text_type=theme_text)

    await send_method(text=f"{template_text}{story}", reply_markup=keyboards.after_text())
