import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from database.roleta_db import DBroleta
from utils.embed import  EmbedPadrao

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$",
                    intents=intents,
                    case_insensitive=True,
                    help_command=None)



@bot.event
async def on_ready():
    DBroleta.criar_tabela()
    print("Bot online com sucesso!")

@bot.event
async def on_command_error(ctx,error):
    from discord.ext import commands

    if isinstance(error,commands.CommandNotFound):
        await ctx.send(embed=EmbedPadrao.erro(
            ctx,
            "Comando não encontrado, Use $ajuda para ver os comandos."
        ))
    else:
        raise error

async def main():
    async with bot:
        await bot.load_extension("cogs.fun")
        await bot.load_extension("cogs.utility")
        await bot.start(token)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bot encerrado manualmente.")


