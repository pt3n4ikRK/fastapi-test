import os
import sqlite3
from pathlib import Path
from threading import Lock


class Database:
    def __init__(self, db_name: str = None):
        # Определяем абсолютный путь к БД
        if not db_name:
            base_dir = Path(__file__).resolve().parent.parent
            db_name = os.path.join(base_dir, "database", "main.db")

        # Создаем директорию если нужно
        os.makedirs(os.path.dirname(db_name), exist_ok=True)

        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.lock = Lock()
        print(f"Database connected: {db_name}")  # Для отладки

    def execute(self, query, params=()):
        with self.lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                self.conn.commit()
                return cursor
            except Exception as e:
                self.conn.rollback()
                raise e

    def __del__(self):
        self.conn.close()