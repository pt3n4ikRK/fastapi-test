import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot_utils.verifySystem import VerifyService
from database.core import Database
from tgbot import dp, bot
import uvicorn

db = Database()
verify = VerifyService(db)



@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task = asyncio.create_task(dp.start_polling(bot))
    print("🚀 Bot started")

    yield # Start FastAPI

    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        print("Polling bot stopped")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/about")
def about():
    return {"info": "This api created using FastAPI"}

@app.get("/verify/{code}")
async def verify_code(code: str):
    users, message = verify.check_code(code)
    print(users)
    await bot.send_message(users, f"{message}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)