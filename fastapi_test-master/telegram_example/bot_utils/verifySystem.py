import random
import sqlite3
import string

from fastapi import HTTPException


class VerifyService:
    def __init__(self, db):
        self.db = db
        self._init_db()

    def _init_db(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS verify_codes (
            code TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL
        )
        """)

        self.db.execute("""
                CREATE TABLE IF NOT EXISTS verify_users (
                    user_id INTEGER PRIMARY KEY
                )
                """)

    def create_code(self, user_id):
        chars = string.ascii_uppercase + string.digits
        for _ in range(3):  # 3 попытки
            code = ''.join(random.choice(chars) for _ in range(6))
            try:
                self.db.execute(
                    "INSERT INTO verify_codes VALUES (?, ?)",
                    (code, user_id)
                )
                return code
            except sqlite3.IntegrityError:
                continue
        raise Exception("Не удалось сгенерировать код")

    def check_code(self, code: str):
        users = self.db.execute(
            "SELECT user_id FROM verify_codes WHERE code = ?",
            (code,)
        )
        try:

            if not users.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail="Код не найден или уже был указан",
                    headers = {"X-Error": "Invalid code"}
                )
            user_id = self.db.execute(
                "SELECT user_id FROM verify_codes WHERE code = ?",
                (code,)
            ).fetchone()[0]
            self.db.execute("INSERT INTO verify_users VALUES (?)", (user_id,))
            self.db.execute("DELETE FROM verify_codes WHERE code = ?", (code,))

            return user_id, "Вы успешно вошли в систему."
        except sqlite3.IntegrityError:
            self.db.execute("DELETE FROM verify_codes WHERE code = ?", (code,))
            raise HTTPException(
                status_code=410,
                detail="Вы уже есть в базе данных",
                headers={"X-Error": "Invalid code"}
            )

    def check_user(self, user_id) -> tuple[bool, str] | bool: # Check Database with verify users
        user = self.db.execute("SELECT 1 FROM verify_users WHERE user_id = ?", (user_id, )).fetchone()
        if user:
            return True, "Вы уже есть в этой базе данных"
        return False