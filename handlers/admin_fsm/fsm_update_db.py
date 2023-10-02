from database.sqlite_db import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keyboards.client_kb import *
from keyboards.admin_kb import *
from config import *
from ldap_connection.active_accounts import *


class FSMUpdate(StatesGroup):
    document = State()


async def start_update_db(message: types.Message):
    """
    :param message:
    :return:

    Обновляет данные в user.db, удаляет уволенных из базы и из чата
    """

    await bot.send_message(admins_chat_id, 'Состовляю список пользователей на удаление...')
    accs_to_delete = ''
    for user in await BotUsersTable.get_all_users_email_from_db():
        if await is_user_email_active(user[0]):
            continue
        else:
            accs_to_delete = accs_to_delete + f"{user[0]} {await BotUsersTable.get_user_full_name(await BotUsersTable.get_user_id(user[0]))}\n"

    with open(f"users_to_delete.txt", 'w') as f:
        f.write(str(accs_to_delete))

    try:
        with open(f"users_to_delete.txt", 'rb') as f:
            await bot.send_document(chat_id=admins_chat_id, document=f)
            await bot.send_message(admins_chat_id,
                                   'Если в списке все правильно, нажмите ОК, если нет, то нажмите изменить, затем отправьте отредактированный файл с тем же названием',
                                   reply_markup=kb_admin_update_db)
    except:
        await bot.send_message(admins_chat_id, 'Удалять некого')


async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(admins_chat_id, 'А, ну ладно...', reply_markup=kb_admin_panel_main)
    await state.finish()


async def aprove_list(message: types.Message, state: FSMContext):
    await bot.send_message(admins_chat_id, 'Начинаю чистку')
    deleted_accounts = []
    for user in await BotUsersTable.get_all_users_email_from_db():
        if await is_user_email_active(user[0]):
            continue
        else:
            try:
                await bot.kick_chat_member(chat_id, await BotUsersTable.get_user_id(user[0]))
                await bot.kick_chat_member(channel_id, await BotUsersTable.get_user_id(user[0]))
            except:
                print("User doesn't exist in chat")

            await BotUsersTable.delete_user(user[0])
            deleted_accounts.append(user[0])

    await bot.send_message(admins_chat_id, f"Удалены: {deleted_accounts}")
    await message.answer('База обновлена!', reply_markup=kb_admin_panel_main)
    await state.finish()


async def edit(message: types.Message, state: FSMContext):
    await bot.send_message(admins_chat_id, 'Отправьте список')
    await FSMUpdate.document.set()


async def get_document(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['document'] = message

    # Download the PDF file
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    downloaded_file = await bot.download_file_by_id(file_id, file_path)
    print(downloaded_file.name)
    await bot.send_message(admins_chat_id, 'Принял')
    accs_to_delete = []
    with open(f"{file_path}", 'rb') as f:
        lines = f.readlines()
        for line_ in lines:
            line = line_.decode('utf8')
            if len(line.strip().split()) == 0:
                continue
            accs_to_delete.append(line.strip().split()[0])
            print(line.strip().split()[0])

    for user in accs_to_delete:
        if await is_user_email_active(user):
            continue
        else:
            try:
                await bot.kick_chat_member(chat_id, await BotUsersTable.get_user_id(user))
                await bot.kick_chat_member(channel_id, await BotUsersTable.get_user_id(user))
            except:
                print("User doesn't exist in chat")
            await BotUsersTable.delete_user(user)

    await bot.send_message(admins_chat_id, f"Удалены: {accs_to_delete}")
    await message.answer('База обновлена!', reply_markup=kb_admin_panel_main)
    await state.finish()


def register_handlers_fsm_admin_update_db(dp: Dispatcher):
    dp.register_message_handler(start_update_db, Text(equals=btn_update_db.text), state=None)
    dp.register_message_handler(cancel, Text(equals=btn_cancel.text), state="*")
    dp.register_message_handler(aprove_list, Text(equals=btn_aprove.text), state="*")
    dp.register_message_handler(edit, Text(equals=btn_edit.text), state="*")
    dp.register_message_handler(get_document, content_types=['document'], state=FSMUpdate.document)
    dp.register_message_handler(cancel, Text(equals=btn_cancel.text), state="*")
