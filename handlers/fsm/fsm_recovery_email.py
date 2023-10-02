import time
from database.sqlite_db import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from mail.send_email import send_letter
from keyboards.client_kb import kb_client


class FSMRecoveryEmail(StatesGroup):
    email_for_answer = State()


async def cm_start3(message: types.Message, state: FSMContext):
    if await BotUsersTable.is_user_exists(message.from_user.id) is not True:
        await message.answer('<b>Вы не авторизованы</b>\n\n'
                             'Отправьте команду /start для авторизации', reply_markup=types.ReplyKeyboardRemove())
    else:
        await FSMRecoveryEmail.email_for_answer.set()
        await message.answer('<b>Введите вашу личную почту</b>\n'
                             'На нее придет письмо с новыми данными для входа\n\n'
                             '<i>отменить заявку - /cancel</i>', reply_markup=types.ReplyKeyboardRemove())


async def load_email_for_answer(message: types.Message, state: FSMContext):
    if '@' in message.text and '.' in message.text:
        async with state.proxy() as data:
            data['email_for_answer'] = message.text
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Сброс пароля от почты'
        letter_reply_email = data['email_for_answer']
        letter_text = "Заявка на восстановление доступа к почте\r\n\n" \
                      f"ФИО: {letter_full_name}\n\n" \
                      f"Почта для восстановления: {letter_email}\n\n" \
                      f"Почта для ответа пользователю: {data['email_for_answer']}\n\n"
        await send_letter('ic-sys-admin@iteco-inno.ru', letter_reply_email, letter_subject, letter_text)
        await message.answer('✅ Заявка отправлена!\n'
                             f'После обработки заявки, ответ придет на почту {data["email_for_answer"]}',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()  # бот выходит из машины состояний и ОЧИЩАЕТ ВЕСЬ СЛОВАРЬ
        time.sleep(2)
        await message.answer('💬 Чем еще я могу вам помочь?', reply_markup=kb_client)
    else:
        await message.answer('Пожалуйста, введите <b>корректную</b> почту\n\n')
        return


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('💬 Чем я могу вам помочь?', reply_markup=kb_client)


def register_handlers_fsm_recovery_email(dp: Dispatcher):
    dp.register_message_handler(cm_start3, Text(equals='✉ Сброс пароля от почты'), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(load_email_for_answer, state=FSMRecoveryEmail.email_for_answer)
