from database.sqlite_db import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keyboards.client_kb import *
from mail.send_email import send_letter_with_attachment
from config import *
from handlers.client_handler import ignore_message_from


class FSMPromo(StatesGroup):
    text = State()
    document = State()


async def promo_send_resume(message: types.Message):
    """
    :param message:
    :return:
    Отправка резюме по программе привели сотрудника в отдел кадро
    """

    if not await BotUsersTable.is_user_exists(message.chat.id):
        return
    if await ignore_message_from(message):
        return
    message1 = """💬 Хотите получить финансовый бонус?

Программа Приведи Сотрудника - это реферальная программа, по которой вы можете получить финансовое вознаграждение до 100 000 рублей, порекомендовав кандидата, который оформится в штат и пройдет испытательный срок(ИС).
Нам всегда нужны разработчики, тестировщики, аналитики!
Для участия прикрепите резюме кандидата.
Я отправлю информацию нужному отделу"""

    message2 = """
📨 Дождитесь информации от HR по результатам собеседования и приема в компанию вашего кандидата.

Получить деньги* можно 2 частями:
✅30% от суммы бонуса после зачисления в штат компании - 1 часть (в течение месяца);
✅70% от суммы бонус после успешного завершения испытательного срока  - 2 часть (по истечению 3х месяцев с даты оформления рекомендованного кандидата) .

* Размер выплаты зависит от роли, на которую кандидат оформляется к нам в компанию. (см. Слайд)
Ты можешь привести любое число сотрудников!

<b>ВАЖНО!</b>
Обращаем Ваше внимание, что в программе может принять участие любой сотрудник группы компаний, который занят в проектной деятельности, кроме должностей в обязательности которых входит непосредственно рост портфеля, а конкретно Бизнес-партнер, Управляющий партнер и Руководитель портфеля проектов.

Если остались вопросы, напишите Алене Резник ( @ic_iteco )"""

    await bot.send_message(message.from_user.id, message1)
    await bot.send_message(message.from_user.id, message2, parse_mode="html")
    promo_file = open(f"{path_to_directory}files_to_send/promo.jpg", 'rb')
    await bot.send_photo(message.from_user.id, promo_file)
    promo_file.close()
    await FSMPromo.text.set()
    message1 = '📄 Укажите должность, на которую направляете резюме и немного расскажите о человеке (его опыт, навыки и т.д.).'
    await bot.send_message(message.from_user.id, message1, reply_markup=kb_client_promo)


async def cancel_get_document(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('💬 Чем я могу вам помочь?', reply_markup=kb_client)


async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await FSMPromo.document.set()
    message1 = '📄 Отправьте резюме кандидата в формате PDF '
    await bot.send_message(message.from_user.id, message1, reply_markup=kb_client_promo)


async def get_document(message: types.Message, state: FSMContext):
    if message.document.mime_type == 'application/pdf':
        async with state.proxy() as data:
            data['document'] = message

        for_letter = ''

        async with state.proxy() as data:
            for_letter = data['text']
        # Download the PDF file
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = await bot.download_file_by_id(file_id, file_path)
        print(downloaded_file.name)
        letter_full_name = await BotUsersTable.get_user_full_name(message.from_user.id)
        letter_email = await BotUsersTable.get_user_email(message.from_user.id)
        letter_subject = 'Анкета по программе "Приведи сотрудника"'
        letter_text = "Анкета по программе 'Приведи сотрудника'\r\n\n" \
                      f"ФИО отправителя: {letter_full_name}\n\n" \
                      f"Почта для уведомления о готовности: {letter_email}\n\n" \
                      f"Cопроводительное письмо: {for_letter}"

        await send_letter_with_attachment(mail_recruiting, letter_email, letter_subject, letter_text,
                                          f"{downloaded_file.name}",
                                          f"Приведи сотрудника. Резюме от {letter_full_name}.pdf")
        await bot.send_message(message.from_user.id, "Анкета отправлена в отдел рекрутинга!", reply_markup=kb_client)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id,
                               "Документ не отправлен, я принимаю только PDF!\nЕсли хотите отправить снова, нажмите кнопку 'Программа Приведи Сотрудника'",
                               reply_markup=kb_client)
        await state.finish()


def register_handlers_fsm_promo(dp: Dispatcher):
    dp.register_message_handler(promo_send_resume, Text(equals=btn_promo.text), state=None)
    dp.register_message_handler(cancel_get_document, Text(equals=btn_cancel.text), state="*")
    dp.register_message_handler(get_text, content_types=['text'], state=FSMPromo.text)
    dp.register_message_handler(get_document, content_types=['document'], state=FSMPromo.document)
    dp.register_message_handler(cancel_get_document, Text(equals=btn_cancel.text), state="*")
