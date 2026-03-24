import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from database.roleta_db import DBroleta
from database.config_db import DBConfig
from utils.embed import EmbedPadrao


load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def get_prefix(bot, message):
    if message.guild is None:
        return "$"

    server_id = message.guild.id
    return DBConfig.get_prefix(server_id)


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
    help_command=None
)


async def global_check(ctx):
    print(f"[CHECK] comando={ctx.command} canal_atual={getattr(ctx.channel, 'id', None)} guild={getattr(ctx.guild, 'id', None)}")

    if ctx.guild is None:
        return True

    if ctx.command and ctx.command.name in ["setprefix", "setchannel", "nyxconfig"]:
        return True

    server_id = ctx.guild.id
    channel_id = DBConfig.get_channel(server_id)

    if channel_id is None:
        return True

    if ctx.channel.id == channel_id:
        return True

    await ctx.send(f"Use os comandos no canal configurado <#{channel_id}>")
    return False


bot.add_check(global_check)


@bot.event
async def on_ready():
    DBroleta.criar_tabela()
    DBConfig.criar_tabela()
    print("Bot online com sucesso!")
    print([command.name for command in bot.commands])


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        prefix = await get_prefix(bot, ctx.message)

        await ctx.send(embed=EmbedPadrao.erro(
            ctx,
            f"Comando não encontrado. Use {prefix}ajuda para ver os comandos."
        ))

    elif isinstance(error, commands.CheckFailure):
        # erro gerado quando o global_check bloqueia o comando
        # a mensagem já foi enviada no próprio check
        return

    else:
        raise error


async def main():
    async with bot:
        await bot.load_extension("cogs.fun")
        await bot.load_extension("cogs.utility")
        await bot.load_extension("cogs.admin")
        await bot.start(token)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bot encerrado manualmente.")