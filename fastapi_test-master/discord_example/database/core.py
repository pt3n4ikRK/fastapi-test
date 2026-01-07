import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "main.db"

class Database:
    def __init__(self):
        """
        Creates a table and checks the specified path so that there are no errors with the database creation -
        will make a given folder from where only the data from this example will be taken for the discord bot.
        Doesn't interfere with the Telegram example and vice versa
        """
        self.DB_PATH = str(DB_PATH)
        Path(self.DB_PATH).parent.mkdir(exist_ok=True, parents=True)
        self._create_table()
    def get_connection(self):
        return sqlite3.connect(self.DB_PATH, check_same_thread=False)

    def init_cursor(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
        return cursor

    def _create_table(self):
        """
        The function responsible for creating the necessary tables.
        :return:
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS verify_codes (
                    user_id INTEGER PRIMARY KEY,
                    code TEXT,
                    channel_id INTEGER,
                    status INTEGER
                )"""
            )
            conn.commit()

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS verify_users (
                    user_id INTEGER PRIMARY KEY
                )"""
            )
            conn.commit()



