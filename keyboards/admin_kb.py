from keyboards.client_kb import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_admin_panel_main = ReplyKeyboardMarkup(resize_keyboard=True)

btn_update_db = KeyboardButton('🔄 Обновить базу')
btn_get_users_list = KeyboardButton('📄 Список пользователей')

kb_admin_panel_main.add(btn_get_users_list).add(btn_update_db)


kb_admin_update_db = ReplyKeyboardMarkup(resize_keyboard=True)
btn_aprove = KeyboardButton('👌 OK')
btn_edit = KeyboardButton('✏️ Изменить')
kb_admin_update_db.add(btn_aprove).add(btn_edit).add(btn_cancel)






