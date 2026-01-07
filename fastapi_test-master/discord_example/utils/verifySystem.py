import random
import sqlite3
import string

from fastapi import HTTPException

from discord_example.database.core import Database


class VerifySystem:
    def __init__(self, db: Database):
        """
        Initialize with the main database so that you don't create a new one /
        or so that there is no rambling between databases. Everything works on the same database with different tables
        :param db: VerifySystem(db)
        """
        self.db = db

    def create_code(self, user_id: int, channel_id: int, status: int = 1 or 0):

        """
        A function for creating code. Where ``user_id``, ``channel_id`` are recorded so that they can be returned later
        and the user can be mentioned in the channel where he/she once wrote this command.
        ``status`` is used to understand what kind of code the user wants, for account deletion or for verification.
         ``1`` - for verification. ``0`` - for deletion. Both True and False

        :param user_id: int:
        :param channel_id: int:
        :param status: 0 or 1. 1 - status for verification. 2 - status for deleting the account:
        :return:
        """

        print("🔵 ВХОД В create_code")  # Control point 1
        chars = string.ascii_uppercase + string.digits
        print(f"🔡 Символы для генерации: {chars}")  # Control Point 2

        for i in range(3):

            # give 3 attempts to randomize the special code
            print(f"🔄 Попытка {i + 1}")  # Checkpoint 3
            code = ''.join(random.choice(chars) for _ in range(6))
            print(f"🎲 Сгенерирован код: {code}")  # Control Point 4

            try:
                with self.db.get_connection() as conn:
                    print("📌 Подключение к БД установлено")  # Control Point 5

                    # Adding code to the database with a special status
                    conn.execute(
                        "INSERT INTO verify_codes VALUES (?, ?, ?, ?)",
                        (user_id, code, channel_id, status)
                    )
                    conn.commit()

                    print("💾 Код сохранён в БД")  # Control Point 6
                    return code
            except sqlite3.IntegrityError as e:
                print(f"⚠ Ошибка Integrity: {e}")
            except Exception as e:
                print(f"🚨 Критическая ошибка: {e}")
                raise

    def check_code(self, code: str) -> tuple[int, int, str]:
        """
        When the user visits the link, the code goes here to further validate the code ``status`` actions.
        Where ``1`` is to activate the account, i.e. verify, where ``0`` is to delete the account.


        :param code: str
        :return:
        """

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Check if the code exists
            cursor.execute(
                "SELECT user_id, channel_id, status FROM verify_codes WHERE code = ?",
                (code,)
            )
            result = cursor.fetchone()

            # Send status that the code has already been found or used
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Код не найден или уже был использован",
                    headers={"X-Error": "Invalid code"}
                )

            user_id = result[0] # I fetch user_id from the table using the fetchone() method
            channel_id = result[1] #I fetch channel_id from the table using the fetchone() method
            status = result[2] #I fetch status from the table using the fetchone() method

            try:
                if status == 1: # if status is 1 - account need activate, else - delete
                    # Add the user to verify_users
                    cursor.execute(
                        "INSERT INTO verify_users (user_id) VALUES (?)",
                        (user_id,)
                    )
                    # Delete the used code
                    cursor.execute(
                        "DELETE FROM verify_codes WHERE code = ?",
                        (code,)
                    )
                    conn.commit()  # Capture the changes
                    return channel_id, user_id, f"успешно вошёл в систему."
                else:
                    # Remove user and code from tables
                    cursor.execute("DELETE FROM verify_users WHERE user_id = ?", (user_id,))
                    cursor.execute(
                        "DELETE FROM verify_codes WHERE code = ?",
                        (code,)
                    )
                    conn.commit() # Capture the changes

                    return channel_id, user_id, f"успешно удалил учётную запись."

            except sqlite3.IntegrityError:
                # If the user already exists in verify_users
                cursor.execute(
                    "DELETE FROM verify_codes WHERE code = ?",
                    (code,)
                )
                conn.commit()  # Фиксируем изменения
                return channel_id, user_id,f"Вы уже есть в данной базе данных"

    def check_user(self, user_id: int) -> bool:
        """Checks if the user is verified."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM verify_users WHERE user_id = ?", (user_id,))
            return cursor.fetchone() is not None