import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot_utils.verifySystem import VerifyService
from database.core import Database

load_dotenv()


db = Database()
verify = VerifyService(db)


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

BASE_URL = os.getenv("BASE_URL")

@dp.message(Command("help"))
async def help_cmd(message: Message):
    user_name = message.from_user.full_name
    await message.reply(f"Hello! {user_name}")


@dp.message(Command("verify"))
async def send_verify_code(message: Message):
    success, text = verify.check_user(user_id=message.from_user.id)
    if success:
        return message.reply(text=text)
    code = verify.create_code(user_id=message.from_user.id)
    await message.reply(f"{BASE_URL}/verify/{code}")

async def main():
    #asyncio.create_task(on_message_verification())
    print("🚀 Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())