from aiogram import types, Dispatcher
import keyboards.client_kb as nav
from keyboards.client_kb import *
from keyboards.inline import *
from database.sqlite_db import UnregisteredTable, BotUsersTable
from handlers.client_handler import ignore_message_from
from config import path_to_directory

ID = None


async def button_content(message: types.message):
    if await ignore_message_from(message):
        return

    if await BotUsersTable.is_user_exists(message.from_user.id) is not True:
        await message.answer('<b>Вы не авторизованы</b>\n\n'
                             'Отправьте команду /start для авторизации', reply_markup=types.ReplyKeyboardRemove())
    else:
        if message.text == btn_templates.text:
            await message.answer('💬 Выберите тип шаблона', reply_markup=nav.kb_client_choose_templates)

        if message.text == '📅 Производственный календарь 2023':
            await message.answer_document(open(f"{path_to_directory}files_to_send/Производственный календарь 2023.pdf", 'rb'),
                                          caption='💬 Высылаю календарь на 2023 год', reply_markup=nav.kb_client)

        if message.text == '✍ Запросить справку / документ':
            await message.answer('💬 Что вас интересует?\n\n👇 Выберите пункт меню', reply_markup=nav.kb_client_docs)

        if message.text == '🎁 Наши плюшки':
            await message.answer('💬 Высылаю ссылку со скидками и спецпредложениями https://map.iteco-inno.ru/promo')

        if message.text == '💌':
            await message.answer(
                'Мы не часто с тобой переписываемся, но я всегда рядом 😊 И в День Спасибо хочу от души поблагодарить тебя за прекрасную работу, за ответственность и творческий подход к любой сложной задаче. Желаю, чтобы мы и дальше работали с энтузиазмом, а каждый день приносил тебе успех и радость!')
            await message.answer('Твой Манул- помощник.🤩')
            await message.answer(
                'P. S. А если ты тоже хочешь кого-то поблагодарить, это можно сделать по ссылке https://map.iteco-inno.ru/thanks')

        # =====================QUEST MENU=====================
        if message.text == 'Менее 3-х месяцев':
            markup_wanna_quest = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup_wanna_quest.add("🎁 Пройти квест")
            markup_wanna_quest.add("❌ Отказаться от квеста")
            await message.answer('🎮 Предлагаю вам пройти квест* для новых сотрудников!\n\n'
                                 '📦 За правильные ответы вы получите <b>подарок</b> - Welcome Pack\n\n'
                                 '<i>*квест состоит из трёх заданий, время прохождения ~5 минут</i>',
                                 reply_markup=markup_wanna_quest)
        if message.text == 'Более 3-х месяцев':
            await message.answer(' 💬 Отлично! Что вас интересует?\n\n👇 Выберите пункт меню', reply_markup=nav.kb_client)

        if message.text == '❌ Отказаться от квеста':
            await message.answer('💬 Что вас интересует?\n\n👇 Выберите пункт меню', reply_markup=nav.kb_client)

        # =====================SUGAR MENU=====================
        if message.text == '⬅ Вернуться в главное меню':
            await message.answer('💬 Что вас интересует?\n\n👇 Выберите пункт меню', reply_markup=nav.kb_client)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(button_content)
