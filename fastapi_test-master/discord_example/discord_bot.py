import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.config import verify

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

BASE_URL = os.getenv("BASE_URL")


@bot.command(name="verify")
async def verify_cmd(ctx):
    """
    Invokes the verify command for the user. By sending the ``verifySystem.create_code()``
    function passing the desired ``user_id``, ``channel_id`` and ``status`` labeled ``1``,
    which indicates that the account should be verified, not deleted
    :param ctx:
    :return:
    """
    print(f"🟢 Вызвана команда verify для {ctx.author.id}")

    try:
        # Check if the user is verified
        if verify.check_user(ctx.author.id):
            return await ctx.send("✅ Вы уже верифицированы!")

        # Generate new code
        code = verify.create_code(
            user_id=ctx.author.id,
            channel_id=ctx.channel.id,
            status=1
        )

        print(f"🔢 Сгенерирован код: {code} со статусом 1")
        await ctx.send(f"🔑 Ваш код верификации: {BASE_URL}/verify/{code}")

    except Exception as e:
        print(f"🔴 Ошибка: {e}")
        await ctx.send("❌ Ошибка при генерации кода")

@bot.command(name="delete")
async def delete_cmd(ctx):
    """
    Invokes the delete command for the user.
    By sending the ``verifySystem.create_code()``
    function passing the required ``user_id``, ``channel_id`` and ``status`` labeled ``0``,
    which indicates that the account should be deleted
    :param ctx:
    :return:
    """
    print(f"🟢 Вызвана команда delete для {ctx.author.id}")

    try:
        # Check if the user is verified
        if not verify.check_user(ctx.author.id):
            return await ctx.send("❌ Вас и так нету в базе данных")

        # Generate new code
        code = verify.create_code(
            user_id=ctx.author.id,
            channel_id=ctx.channel.id,
            status=0
        )

        print(f"🔢 Сгенерирован код: {code} со статусом 0")
        await ctx.send(f"🔑 Ваш код для удаления учётной записи: {BASE_URL}/verify/{code}")

    except Exception as e:
        print(f"🔴 Ошибка: {e}")
        await ctx.send("❌ Ошибка при генерации кода")


@bot.command(name="info")
async def info(ctx):
    await ctx.send("Hello!!")



