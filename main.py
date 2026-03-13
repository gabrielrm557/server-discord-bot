import discord
import random
from discord.ext import commands
from deep_translator import GoogleTranslator


token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print("Bot online!")

@bot.command(aliases=["p"])
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(aliases=["foto","f"])
async def avatar(ctx,member:discord.Member):
    await ctx.send(member.avatar.url)

@bot.command(aliases=["es","Es","ES","eS"])
async def espanhol(ctx, *, texto):
    traducao = GoogleTranslator(source='auto', target="es").translate(texto)
    await ctx.send(traducao)

@bot.command(aliases=["pt","Pt","pT",'PT'])
async def portugues(ctx, *, texto):
    traducao = GoogleTranslator(source='auto', target="pt").translate(texto)
    await ctx.send(traducao)

@bot.command(aliases=["en","EN","En","eN"])
async def ingles(ctx, *, texto):
    traducao = GoogleTranslator(source='auto', target="en").translate(texto)
    await ctx.send(traducao)

@bot.command(aliases=["ayuda"])
async def ajuda(ctx):
    await ctx.send("Meu comandos são : $PING , $EN , $ES , $PT , $AVATAR @ ",)

@bot.command()
async def cor(ctx, cor: str):

    cores = {
        "vermelho": "vermelho",
        "rojo": "vermelho",

        "azul": "azul",

        "verde": "verde",

        "roxo": "roxo",
        "morado": "roxo",

        "rosa": "rosa",

        "amarelo": "amarelo",
        "amarillo": "amarelo"
    }

    cor = cor.lower()

    if cor not in cores:
        await ctx.send("🎨 Cores disponíveis:\nvermelho/rojo, azul, verde, roxo/morado, rosa, amarelo/amarillo")
        return

    cor_final = cores[cor]

    cores_roles = ["vermelho", "azul", "verde", "roxo", "rosa", "amarelo"]

    # remover cores antigas
    for role in ctx.author.roles:
        if role.name.lower() in cores_roles:
            await ctx.author.remove_roles(role)

    # pegar cargo da nova cor
    role = discord.utils.get(ctx.guild.roles, name=cor_final)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"🎨 Sua cor agora é **{cor_final}**!")
    else:
        await ctx.send("Cargo de cor não encontrado.")

@bot.command()
async def quem(ctx, *, pergunta):
    membros = [m for m in ctx.guild.members if not m.bot]
    escolhido = random.choice(membros)

    await ctx.send(f"{pergunta}\n é : {escolhido.mention}")


bot.run(token)

