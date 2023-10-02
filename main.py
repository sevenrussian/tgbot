import logging

import handlers.client_handler
from database import sqlite_db
from aiogram.utils import executor
from create_bot import dp, bot
from handlers import msg_handler
from handlers.fsm import fsm_registration, fsm_recovery_email, fsm_quest, fsm_promo
from handlers.admin_fsm import fsm_update_db


# TODO: logging

async def on_startup(_):
    print('Bot is online')
    sqlite_db.sql_start()


logging.basicConfig(level=logging.INFO)

fsm_update_db.register_handlers_fsm_admin_update_db(dp)
handlers.client_handler.register_callback_query(dp)
fsm_quest.register_handlers_fsm_quest(dp)
fsm_promo.register_handlers_fsm_promo(dp)
fsm_recovery_email.register_handlers_fsm_recovery_email(dp)
fsm_registration.register_handlers_fsm_registration(dp)
msg_handler.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
