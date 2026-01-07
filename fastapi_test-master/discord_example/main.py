import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from discord_bot import bot
from utils.config import verify  # Импортируем общие объекты

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Launch the bot on startup
    asyncio.create_task(bot.start(os.getenv("TOKEN")))
    print("Bot started")
    yield #Continuing with FastAPI

    # Stop the bot on completion
    await bot.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "FastAPI + Discord Bot работает!"}

@app.get("/verify/{code}")
async def verify_code(code: str):
    """
    Sends the code from the link to the ``verifySystem.check_code()`` function, which validates this code and sends a message to the user
    :param code:
    :return:
    """
    channel, user, message = verify.check_code(code)
    channel_id = bot.get_channel(channel)
    member = await bot.fetch_user(user)

    await channel_id.send(f"**{member.mention}** {message}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)