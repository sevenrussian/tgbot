from keyboards.admin_kb import *
from ldap_connection.active_accounts import *
from database.sqlite_db import *
from aiogram import Dispatcher, types
from create_bot import dp, bot
from config import chat_id, channel_id, path_to_directory
from config import admins_chat_id


@dp.message_handler(commands='admin')
async def admin(message: types.Message):
    """
    :param message:
    :return:

    Открытие главной админской панели
    """
    if message.chat.id == admins_chat_id:
        await bot.send_message(admins_chat_id, 'Admin panel', reply_markup=kb_admin_panel_main)
    else:
        pass


# @dp.message_handler(text=btn_update_db.text)
# async def admin_update_db(message: types.Message):
#     """
#     :param message:
#     :return:
#
#     Функция кнопки "Обновить базу"
#     """
#     if message.chat.id == admins_chat_id:
#         await bot.send_message(admins_chat_id, 'Обновляю базу...')
#         await update_db(message)
#     else:
#         pass


@dp.message_handler(text=btn_get_users_list.text)
async def get_users_list(message: types.Message):
    if message.chat.id == admins_chat_id:
        users = ''
        for user in await BotUsersTable.get_all_users_email_from_db():
            users = users + f"{user[0]} : {await BotUsersTable.get_user_full_name(await BotUsersTable.get_user_id(user[0]))}\n"

        with open(f"{path_to_directory}users_list.txt", 'w') as f:
            f.write(str(users))

        with open(f"{path_to_directory}users_list.txt", 'rb') as f:
            await bot.send_document(chat_id=admins_chat_id, document=f)

    else:
        pass


# async def update_db(message: types.Message):
#     """
#     :param message:
#     :return:
#
#     Обновляет данные в user.db, удаляет уволенных из базы и из чата
#     """
#     deleted_accounts = []
#     for user in await BotUsersTable.get_all_users_email_from_db():
#         if await is_user_email_active(user[0]):
#             continue
#         else:
#             print(user[0], "doesn't exists in active and deleted")
#             try:
#                 await bot.kick_chat_member(chat_id, await BotUsersTable.get_user_id(user[0]))
#                 await bot.kick_chat_member(channel_id, await BotUsersTable.get_user_id(user[0]))
#             except:
#                 print("User doesn't exist in chat")
#
#             await BotUsersTable.delete_user(user[0])
#             deleted_accounts.append(user[0])
#
#     await bot.send_message(admins_chat_id, f"Удалены: {deleted_accounts}")
#     await bot.send_message(admins_chat_id, 'База обновлена!')
