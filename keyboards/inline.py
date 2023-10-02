from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

urlkb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
paid_vacation_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
unpaid_vacation_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
letter_of_employment_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
recovery_mail_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
copy_employment_history_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)

urlButton = InlineKeyboardButton(text='Отправить заявку', callback_data='ndfl_request')
urlButton2 = InlineKeyboardButton(text='Отменить заявку', callback_data='docs_menu')
urlButton4 = InlineKeyboardButton(text='Отправить заявку', callback_data='unpaid_vacation_request')
urlButton5 = InlineKeyboardButton(text='Отправить заявку', callback_data='paid_vacation_request')
urlButton6 = InlineKeyboardButton(text='Отправить заявку', callback_data='letter_of_employment')
urlButton7 = InlineKeyboardButton(text='Отправить заявку', callback_data='recovery_mail')
urlButton8 = InlineKeyboardButton(text='Отправить заявку', callback_data='employment_history_request')
urlButton76 = InlineKeyboardButton(text='Отправить заявку', callback_data='employment_history_request')
urlButton90 = InlineKeyboardButton(text='Отправить заявку', callback_data='employment_history_request')
urlkb.add(urlButton, urlButton2)

paid_vacation_ikb.add(urlButton5, urlButton2)

unpaid_vacation_ikb.add(urlButton4, urlButton2)

letter_of_employment_ikb.add(urlButton6, urlButton2)

recovery_mail_ikb.add(urlButton7, urlButton2)

copy_employment_history_ikb.add(urlButton8, urlButton2,urlButton76,urlButton90)