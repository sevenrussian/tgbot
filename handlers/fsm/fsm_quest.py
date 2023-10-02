import time
from database.sqlite_db import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from mail.send_email import send_letter
from keyboards.client_kb import kb_client, kb_client_docs


class FSMQuest(StatesGroup):
    numbers_of_sections = State()
    support_email = State()
    secret_word = State()


async def cm_start_quest(message: types.Message):
    if await BotUsersTable.is_user_exists(message.from_user.id) is not True:
        await message.answer('<b>Вы не авторизованы</b>\n\n'
                             'Отправьте команду /start для авторизации',
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await FSMQuest.numbers_of_sections.set()
        await message.answer('<b>🎯 Задание <i>1/3</i></b>\n'
                             'Посчитайте количество пунктов меню в шапке на сайте map.iteco-inno.ru\n\n'
                             'Отправьте в ответ цифру\n\n'
                             '<i>отменить квест - /cancel</i>', reply_markup=types.ReplyKeyboardRemove())


async def cancel_quest(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('💬 Чем я могу вам помочь?', reply_markup=kb_client)


async def load_numbers_of_sections(message: types.Message, state: FSMContext):
    if message.text == '4' or message.text == 'четыре' or message.text == 'Четыре':
        async with state.proxy() as data:
            data['numbers_of_sections'] = message.text
        await FSMQuest.next()
        await message.answer('✅ Правильный ответ!')
        await message.answer('<b>🎯 Задание <i>2/3</i></b>\n'
                             'Подпишитесь на наш информационный канал в тг: t.me/+R5gPs2m10UbiyXL3\n\n'
                             '📌 В одном из закрепленных сообщений канала вы найдете ответ на вопрос ниже\n\n'
                             'На какую почту следует написать, если не работает компьютер?\n\n'
                             '<i>отменить квест - /cancel</i>', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('❌ Неверный ответ, попробуйте еще раз\n\n'
                             '<i>отменить квест - /cancel</i>')
        return


async def load_support_email(message: types.Message, state: FSMContext):
    if message.text == 'support@iteco-inno.ru' or message.text == 'Support@iteco-inno.ru':
        async with state.proxy() as data:
            data['support_email'] = message.text
        await FSMQuest.next()
        await message.answer('✅ Правильный ответ!')
        await message.answer('<b>🎯 Задание <i>3/3</i></b>\n'
                             'Познакомьтесь с нами в VK: clck.ru/rcQfC\n\n'
                             'Ваш нужно найти кодовое слово в описании группы и прислать его в ответ!\n\n'
                             '<i>отменить квест - /cancel</i>', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('❌ Неверный ответ, попробуйте еще раз\n\n'
                             '<i>отменить квест - /cancel</i>')
        return


async def load_secret_word(message: types.Message, state: FSMContext):
    if message.text == 'инновация' or message.text == 'Инновация':
        async with state.proxy() as data:
            data['secret_word'] = message.text
        await message.answer('✅ Правильный ответ!')
        await message.answer('🔥 Поздравляем, вы стали частью команды ГК ИЦ АйТеко!\n\n'
                             'Ожидайте, скоро с вами свяжутся по почте для отправки подарка')
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Прохождение квеста'
        letter_text = "Прохождение квеста\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта: {letter_email}\n\n" \
                      f"Кол-во разделов на сайте: {data['numbers_of_sections']}\n\n" \
                      f"Кому писать, если не работает комп: {data['support_email']}\n\n" \
                      f"Кодовое слово: {data['secret_word']}\n\n"
        await send_letter('a.reznik@iteco-inno.ru', letter_email, letter_subject, letter_text)
        # await send_letter('sallings@i-teco.ru', letter_email, letter_subject, letter_text)
    else:
        await message.answer('❌ Неверный ответ, попробуйте еще раз\n\n'
                             '<i>отменить квест - /cancel</i>')
        return

    await state.finish()
    time.sleep(2)
    await message.answer('💬 Чем я могу вам помочь?', reply_markup=kb_client)


def register_handlers_fsm_quest(dp: Dispatcher):
    dp.register_message_handler(cm_start_quest, Text(equals='🎁 Пройти квест'), state=None)
    dp.register_message_handler(cancel_quest, state="*", commands=['cancel'])
    dp.register_message_handler(load_numbers_of_sections, state=FSMQuest.numbers_of_sections)
    dp.register_message_handler(load_support_email, state=FSMQuest.support_email)
    dp.register_message_handler(load_secret_word, state=FSMQuest.secret_word)
