import sqlite3 as sq
import datetime
from config import path_to_directory


def sql_start():
    global base, cur
    base = sq.connect(f"{path_to_directory}users.db")
    cur = base.cursor()
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS bot_users(tg_id INTEGER, full_name TEXT, email TEXT, '
                 'otp_message INTEGER, user_OTP INTEGER, joing_date timestamp)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS unregistered_users(tg_id INTEGER, joing_date timestamp)')
    base.commit()


class UnregisteredTable:
    @staticmethod
    async def add_user(tg_id):
        cur.execute('INSERT INTO unregistered_users VALUES (?, ?)', (int(tg_id), datetime.datetime.now()))
        base.commit()

    @staticmethod
    async def delete_user(tg_id):
        try:
            sqlite_select_query = """SELECT * from unregistered_users where tg_id = ?"""
            cur.execute(sqlite_select_query, (tg_id,))
            record = cur.fetchone()
            if record is None:
                return
            else:
                sqlite_select_query = """DELETE FROM unregistered_users WHERE tg_id = ?"""
                cur.execute(sqlite_select_query, (tg_id,))
                base.commit()
        except sq.Error as error:
            print("Failed to delete user by tg_id from sqlite table unregistered_users: ", error)


class BotUsersTable:

    @staticmethod
    async def add_user(state):
        async with state.proxy() as data:
            cur.execute('INSERT INTO bot_users VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
            base.commit()

    @staticmethod
    async def is_user_exists(tg_id) -> bool:
        try:
            sqlite_select_query = """SELECT * from bot_users where tg_id = ?"""
            record = cur.execute(sqlite_select_query, (tg_id,)).fetchone()
            if record is None:
                return False
            else:
                return True
        except sq.Error as error:
            print("Failed to read single row from sqlite table", error)
            return False

    @staticmethod
    async def get_user_full_name(tg_id):
        try:
            sqlite_select_query = """SELECT full_name from bot_users where tg_id = ?"""
            cur.execute(sqlite_select_query, (tg_id,))
            record = cur.fetchone()
            if record is None:
                return False
            else:
                return record[0]
        except sq.Error as error:
            print("Failed to read single row from sqlite table", error)

    @staticmethod
    async def get_user_email(tg_id) -> str:
        try:
            sqlite_select_query = """SELECT email from bot_users where tg_id = ?"""
            cur.execute(sqlite_select_query, (tg_id,))
            record = cur.fetchone()
            if record is None:
                return ""
            else:
                return record[0]
        except sq.Error as error:
            print("Failed to read single row from sqlite table", error)

    @staticmethod
    async def is_user_has_email(tg_id) -> bool:
        try:
            sqlite_select_query = """SELECT email from bot_users where tg_id = ?"""
            cur.execute(sqlite_select_query, (tg_id,))
            record = cur.fetchone()
            if record[0] == '':
                return False
            else:
                return True
        except sq.Error as error:
            print("Failed to read single row from sqlite table", error)

    @staticmethod
    async def delete_user(user_email):
        try:
            sqlite_select_query = """SELECT * from bot_users where email = ?"""
            cur.execute(sqlite_select_query, (user_email,))
            record = cur.fetchone()
            if record is None:
                return False
            else:
                sqlite_select_query = """DELETE FROM bot_users WHERE email = ?"""
                cur.execute(sqlite_select_query, (user_email,))
                base.commit()
                return True
        except sq.Error as error:
            print("Failed to delete user by email from sqlite table", error)
            return False

    @staticmethod
    async def delete_user_by_id(user_id):
        try:
            sqlite_select_query = """SELECT * from bot_users where tg_id = ?"""
            cur.execute(sqlite_select_query, (user_id,))
            record = cur.fetchone()
            if record is None:
                return False
            else:
                sqlite_select_query = """DELETE FROM bot_users WHERE tg_id = ?"""
                cur.execute(sqlite_select_query, (user_id,))
                base.commit()
                return True
        except sq.Error as error:
            print("Failed to delete user by tg_id from sqlite table", error)
            return False

    @staticmethod
    async def get_all_users_email_from_db() -> list:
        return cur.execute("SELECT email FROM bot_users").fetchall()

    @staticmethod
    async def get_user_id(user_email) -> int:
        sqlite_select_query = """SELECT tg_id FROM bot_users WHERE email = ?"""
        return int(cur.execute(sqlite_select_query, (user_email,)).fetchone()[0])

    @staticmethod
    async def get_all_tg_id() -> list:
        ids = []
        for data in cur.execute("SELECT tg_id FROM bot_users").fetchall():
            ids.append(data[0])
        return ids
