import datetime
import time
from aiogram import Dispatcher, types
from create_bot import dp, bot
from mail.send_email import send_letter
from database.sqlite_db import UnregisteredTable, BotUsersTable
from keyboards.client_kb import *
from config import mail_hr_department, chat_id, mail_ndfl


async def main_menu(call: types.CallbackQuery):
    if await ignore_message_from_call(call):
        return
    await call.message.answer(text="💬 Чем я могу вам помочь?", reply_markup=kb_client_docs)


async def docs_menu(call: types.CallbackQuery):
    if await ignore_message_from_call(call):
        return
    await call.message.answer(text="💬 Чем я могу вам помочь?", reply_markup=kb_client_docs)


@dp.message_handler(content_types=["new_chat_members"])
async def greetings_to_new_member(message: types.Message):
    if message.chat.id == chat_id:
        if await BotUsersTable.is_user_exists(message.chat.id):
            return
        await UnregisteredTable.add_user(message.from_user.id)
        print("New user in chat: ", message.from_user.id)


@dp.message_handler(text='my_id')
async def get_id(message: types.Message):
    await bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(text=btn_news_n_navigator.text)
async def news_n_navigator(message: types.Message):
    """
    :param message:
    :return:

    Новости, база знаний, отправка календаря
    """
    if await BotUsersTable.is_user_exists(message.from_user.id):
        if await ignore_message_from(message):
            return
        message1 = '💬 Хотите следить за внутрикорпоративными новостями компании?\n\n' \
                   'Перейдите по ссылке: map.iteco-inno.ru\n\n' \
                   'А еще для сотрудников у нас есть:\n\n' \
                   'ТГ-канал Информатор:\nhttps://t.me/+R5gPs1cjZQdQx2ns\n' \
                   'Чат-болталка:\nhttps://t.me/+WNcLX2cflpA1MWNi\n\n' \
                   '🌐 Соцсети\n' \
                   '💬 Следи за новостями!\n\n' \
                   'VK: clck.ru/qBmBw\n' \
                   'YouTube: clck.ru/ovNJv\n' \
                   'Telegram компании: https://t.me/iciteco_official\n'
        await bot.send_message(message.from_user.id, message1, reply_markup=kb_news_n_navigator)


@dp.message_handler(text=btn_knowlage_base.text)
async def knowledge_base(message: types.Message):
    if await BotUsersTable.is_user_exists(message.from_user.id):
        if await ignore_message_from(message):
            return
        message1 = '🧠 База знаний\n' \
                   '💬 Хотите записаться на мини-курсы по soft skills & hard skills?\n\n' \
                   'Перейдите по ссылке:\n' \
                   'map.iteco-inno.ru/it-courses'
        await bot.send_message(message.from_user.id, message1, reply_markup=kb_client)


async def send_ndfl_request(call: types.CallbackQuery):
    if await ignore_message_from_call(call):
        return
    letter_full_name = await BotUsersTable.get_user_full_name(call.from_user.id)
    letter_email = await BotUsersTable.get_user_email(call.from_user.id)
    letter_subject = 'Заявка на Справку 2НДФЛ'
    letter_text = "Заявка на Справку 2НДФЛ\r\n\n" \
                  f"ФИО: {letter_full_name}\n\n" \
                  f"Почта для уведомления о готовности: {letter_email}"
    # TODO
    await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
    await call.answer(text="Заявка отправлена!", show_alert=True)
    time.sleep(2)
    await call.message.answer('💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


async def send_unpaid_vacation_request(call: types.CallbackQuery):
    if await ignore_message_from_call(call):
        return
    letter_full_name = await BotUsersTable.get_user_full_name(call.from_user.id)
    letter_email = await BotUsersTable.get_user_email(call.from_user.id)
    letter_subject = 'Заявка на получение шаблона заявления'
    letter_text = "Заявка на получение шаблона заявления\r\n\n" \
                  f"ФИО: {letter_full_name}\n\n" \
                  f"Почта для уведомления о готовности: {letter_email}\n\n" \
                  f"Шаблон заявления: Неоплачиваемый отпуск"
    await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
    await call.answer(text="Заявка отправлена!", show_alert=True)
    time.sleep(2)
    await call.message.answer('💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


async def send_paid_vacation_request(call: types.CallbackQuery):
    if await ignore_message_from_call(call):
        return
    letter_full_name = await BotUsersTable.get_user_full_name(call.from_user.id)
    letter_email = await BotUsersTable.get_user_email(call.from_user.id)
    letter_subject = 'Заявка на получение шаблона заявления'
    letter_text = "Заявка на получение шаблона заявления\r\n\n" \
                  f"ФИО: {letter_full_name}\n\n" \
                  f"Почта для уведомления о готовности: {letter_email}\n\n" \
                  f"Шаблон заявления: Оплачиваемый отпуск"
    await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
    await call.answer(text="Заявка отправлена!", show_alert=True)
    time.sleep(2)
    await call.message.answer('💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text=btn_reference.text)
async def reference(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на справку с места работы'
        letter_text = "Заявка на справку с места работы\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text=btn_reference_with_income.text)
async def reference_with_income(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на справку с места работы'
        letter_text = "Заявка на справку с места работы c доходом\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text=btn_tk_copy.text)
async def copy_employment_tk(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на копию трудовой книжки'
        letter_text = "Заявка на копию трудовой книжки незаверенная\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text=btn_tk_copy_approved.text)
async def copy_employment_tk_approved(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на копию трудовой книжки'
        letter_text = "Заявка на копию трудовой книжки заверенная\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text=btn_ndfl.text)
async def get_ndfl(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на Справка 2-НДФЛ'
        letter_text = "Заявка на Справка 2-НДФЛ\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_ndfl, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text='Оплачиваемый отпуск')
async def get_paid(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на Оплачиваемый отпуск'
        letter_text = "Заявка на Оплачиваемый отпуск\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


@dp.message_handler(text='Неоплачиваемый отпуск')
async def get_unpaid(message: types.Message):
    if await ignore_message_from(message):
        return
    if await BotUsersTable.is_user_exists(message.from_user.id):
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Заявка на Неоплачиваемый отпуск'
        letter_text = "Заявка на Неоплачиваемый отпуск\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}"
        await send_letter(mail_hr_department, letter_email, letter_subject, letter_text)
        await bot.send_message(message.from_user.id, "Заявка отправлена!")
        await bot.send_message(message.from_user.id, '💬 Всегда рад помочь! Что-то еще?', reply_markup=kb_client)


async def ignore_message_from(message: types.Message) -> bool:
    if message.chat.id == chat_id:
        return True
    else:
        return False


async def ignore_message_from_call(call: types.CallbackQuery) -> bool:
    if call.message.chat.id == chat_id:
        return True
    else:
        return False


def register_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu, text='main_menu')
    dp.register_callback_query_handler(docs_menu, text='docs_menu')
    dp.register_callback_query_handler(send_ndfl_request, text='ndfl_request')
    dp.register_callback_query_handler(send_unpaid_vacation_request, text='unpaid_vacation_request')
    dp.register_callback_query_handler(send_paid_vacation_request, text='paid_vacation_request')
