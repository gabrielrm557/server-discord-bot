import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from database.roleta_db import DBroleta

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$",
                    intents=intents,
                    case_insensitive=True)



@bot.event
async def on_ready():
    DBroleta.criar_tabela()
    print("Bot online com sucesso!")


async def main():
    async with bot:
        await bot.load_extension("cogs.fun")
        await bot.load_extension("cogs.utility")
        await bot.start(token)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bot encerrado manualmente.")


