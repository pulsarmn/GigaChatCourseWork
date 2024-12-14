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


@user_router.message(CommandStart())
@user_router.message(F.text == 'Главное меню')
async def start_menu(message: Message, state: FSMContext):
    await database.add_user(message.from_user.id)

    user_data = await database.get_user_data(message.from_user.id)
    is_premium = user_data[2]

    await message.answer(
        text=f'Привет, {message.from_user.first_name}! Я бот GigaChat, я могу генерировать код и объяснения к нему '
             f'\nВыбери действие:',
        reply_markup=keyboards.start_menu(is_premium=is_premium))
    await state.clear()


@user_router.callback_query(F.data == 'generate_random_code')
async def code_random(callback: CallbackQuery, state: FSMContext):
    prompt_text = random.choice(list(prompts_text.keys()))
    await send_text(callback, state, theme_text=prompt_text)


@user_router.callback_query(F.data == 'generate_code_on_query')
async def ask_for_query(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите запрос:")
    await state.set_state(UserStates.waiting_for_query)


@user_router.message(UserStates.waiting_for_query)
async def generate_code_from_query(message: Message, state: FSMContext):
    user_query = message.text

    try:
        await database.process_user_query(message.from_user.id)
    except Exception:
        await message.answer(
            text='У вас закончились бесплатные запросы! Для дальнейшего использования необходимо купить подписку!',
            reply_markup=keyboards.buy_sub()
        )
        await state.clear()
        return

    story = create_random_text(user_query, is_query=True)
    await message.answer(f"Результат запроса:\n{story}", reply_markup=keyboards.after_text())

    await state.clear()


@user_router.callback_query(F.data == 'personal_cabinet')
async def user_info(callback: CallbackQuery):
    user_info = await database.get_user_data(callback.from_user.id)
    is_premium = bool(user_info[2])
    text = f'Информация о пользователе:\nusername: @{callback.from_user.username}\nОсталось запросов: '
    text += 'неограничено' if is_premium else f'{user_info[1]} из 20'

    kb = None if is_premium else keyboards.buy_sub()
    await callback.message.answer(text=text, reply_markup=kb)


@user_router.callback_query(F.data == 'sub')
async def buy_sub(callback: CallbackQuery):
    payment_id = str(uuid.uuid4())
    await callback.message.answer_invoice(
        title='Подписка на безлимитные запросы',
        description='Подписка на безлимитные запросы',
        payload=payment_id,
        provider_token=config.payment_token,
        currency='RUB',
        prices=[LabeledPrice(label='Оплата услуг', amount=29990)])
    await callback.message.answer(text='Номер карты для теста: 5555 5555 5555 5555')


@user_router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery):
    print('pre_checkout')
    await query.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


@user_router.message(F.successful_payment)
async def success_payment_handler(message: Message):
    await database.set_premium(message.from_user.id)
    await message.answer(text='Спасибо за покупку подписки!\nПользуйтесь ботом без ограничений!')

