import time
import math
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from keyboards.client_kb import kb_client
from mail.send_email import send_letter
from database.sqlite_db import *
import re
from string import ascii_letters
from handlers.admin_handler import *
from handlers.client_handler import ignore_message_from
import datetime


class FSMRegistration(StatesGroup):
    full_name = State()
    email = State()
    user_OTP = State()
# TODO:

async def cmd_start(message: types.Message):
    if await ignore_message_from(message):
        return

    if (await BotUsersTable.is_user_exists(message.from_user.id)) and (
    await BotUsersTable.is_user_has_email(message.from_user.id)):

        await message.answer('💬 Чем я могу вам помочь?', reply_markup=kb_client)
    else:

        await FSMRegistration.email.set()
        await message.reply("👋 Привет! Я Манул - помощник ИЦ Ай-Теко\n\n"
                            "Я доступен только для сотрудников компании, поэтому вам нужно авторизоваться\n\n"
                            "<b>Введите вашу корпоративную почту</b>\n\n"
                            "На почту придет код подтверждения\n\n"
                            "<i>не знаете почту?</i>\n"
                            "<i>напишите вашему руководителю проекта</i>\n\n"
                            "<i>не знаете руководителя проекта?</i>\n"
                            "<i>напишите @ic_iteco</i>", reply_markup=types.ReplyKeyboardRemove())


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


async def has_english(text):
    return bool(re.search('[a-zA-Z]', text))


async def has_number(text):
    return bool(re.search('[0-9]', text))


async def load_email(message: types.Message, state: FSMContext):
    if ('@iteco-inno.ru' in message.text or '@i-teco.ru' in message.text) and (
            await has_cyrillic(message.text) is False) \
            and await has_number(message.text) is False and (message.text != '@iteco-inno.ru') and (
            message.text != '@i-teco.ru') \
            and (message.text != '@@i-teco-inno.ru') and (message.text != '@@i-teco.ru') and ',' not in message.text:

        if await is_user_email_active(message.text.strip()):
            async with state.proxy() as data:
                data['tg_id'] = message.from_user.id
            async with state.proxy() as data:
                data['full_name'] = await get_username_from_ad(message.text)
            await FSMRegistration.next()
            async with state.proxy() as data:
                data['email'] = message.text
            user_email = data['email']
            digits = "0123456789"
            OTP = ""
            otp_message = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
            otp_message = "Ваш одноразовый код: " + OTP
            async with state.proxy() as data:
                data['otp_message'] = OTP
            global otp_code
            otp_code = OTP
            letter_subject = 'Подтверждение учетной записи'
            await send_letter(f"{user_email}", f"{user_email}", letter_subject, str(otp_message))
            await message.reply(f"На почту {data['email']} был выслан одноразовый код подтверждения\n\n"
                                f"<b>Введите код подтверждения</b>\n\n"
                                f"<i>начать регистрацию заново - /retry</i>")
        else:
            await bot.send_message(message.from_user.id,
                                   "Пользователь с такой почтой не найден(\nПожалуйста, проверьте корректность написания почты либо попробуйте позже")

    else:
        await message.reply('Пожалуйста, введите корректные данные')
        return


async def process_user_OTP(message: types.Message, state: FSMContext):
    if message.text != otp_code:
        await message.answer('Неверный код, попробуйте снова\n\n'
                             '<b>Введите код подтверждения</b>\n\n')
        return
    else:
        async with state.proxy() as data:
            data['user_OTP'] = message.text
        markup = types.ReplyKeyboardRemove()
        await message.answer('Вы авторизованы!')

        await UnregisteredTable.delete_user(message.from_user.id)

        async with state.proxy() as data:
            data['joing_date'] = datetime.datetime.now()

        await BotUsersTable.add_user(state)
        await state.finish()

        markup_how_long = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup_how_long.add("Более 3-х месяцев")
        markup_how_long.add("Менее 3-х месяцев")

        await message.answer('💬 Как долго вы работаете в компании?', reply_markup=markup_how_long)


async def cancel_registration_handler(message: types.Message, state: FSMContext):
    if await BotUsersTable.is_user_exists(message.from_user.id) is not True:
        await message.answer('<b>Вы не авторизованы</b>\n\n'
                             'Отправьте команду /start для авторизации', reply_markup=types.ReplyKeyboardRemove())
    else:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('💬 Чем я могу вам помочь?', reply_markup=kb_client)


def register_handlers_fsm_registration(dp: Dispatcher):
    dp.register_message_handler(cmd_start, state=None, commands=['start'])
    dp.register_message_handler(cmd_start, state='*', commands=['retry'])
    dp.register_message_handler(load_email, state=FSMRegistration.email)
    dp.register_message_handler(process_user_OTP, state=FSMRegistration.user_OTP)
