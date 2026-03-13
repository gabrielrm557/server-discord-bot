import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
import os
from deep_translator import GoogleTranslator

load_dotenv()
token = os.getenv("TOKEN")
print(token)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$",
                    intents=intents,
                    case_insensitive=True)

@bot.event
async def on_ready():
    print("Bot online!")

@bot.command(aliases=["p"])
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(aliases=["foto","f"])
async def avatar(ctx,member:discord.Member = None):
    if member is None:
        member = ctx.author
    await ctx.send(member.avatar.url)

@bot.command(aliases=["es"])
async def espanhol(ctx, *, texto):
    traducao = GoogleTranslator(source='auto', target="es").translate(texto)
    await ctx.send(traducao)

@bot.command(aliases=["pt"])
async def portugues(ctx, *, texto):
    traducao = GoogleTranslator(source='auto', target="pt").translate(texto)
    await ctx.send(traducao)

@bot.command(aliases=["en"])
async def ingles(ctx, *, texto):
    traducao = GoogleTranslator(source='auto', target="en").translate(texto)
    await ctx.send(traducao)

@bot.command(aliases=["ayuda"])
async def ajuda(ctx):
    await ctx.send("📖 **Comandos do Bot**\n\n"
        "🏓 **$ping** → Verifica se o bot está online\n\n"
        
        "🌎 **Tradução:**\n"
        "$en <texto> → Traduz para inglês\n"
        "$es <texto> → Traduz para espanhol\n"
        "$pt <texto> → Traduz para português\n\n"
        
        "👤 **$avatar [@usuario]** → Mostra o avatar de um usuário (ou o seu se não marcar ninguém)\n\n"
        
        "🎲 **$roleta** → Jogue roleta russa (1/6 de chance de ser silenciado)\n\n"
        
        "🎱 **$8ball <pergunta>** → Faça uma pergunta e receba uma resposta aleatória\n\n"
        
        "📰 **$update** → Mostra as últimas atualizações do bot"
    )

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

@bot.command(aliases=["8ball"])
async def ball(ctx):
    lista = ['sim','não','talvez']
    await ctx.send(random.choice(lista))

@bot.command()
async def update(ctx):
    with open("changelog.md") as change:     
        await ctx.send(change.read())

@bot.command()
async def roleta(ctx):
    resultado = random.randint(1,6)
    print(resultado)
    morte = 1
    if resultado == morte:
        embed = discord.Embed(
        title="🎲 Roleta Russa",
        description="💥 BANG! Você morreu e foi silenciado por 30s",
        color= discord.Color.red()
    )
        arquivo = discord.File("images/morreu.png", filename="morreu.png")
        embed.set_image(url="attachment://morreu.png")
        embed.set_footer(text=f"Executado por {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        try:
            await ctx.author.timeout(timedelta(seconds=30))
        except discord.errors.Forbidden:
            print("Erro de permissão")
        await ctx.send(embed=embed,file=arquivo)

    else:
            embed = discord.Embed(
            title="🎲 Roleta Russa",
            description="*click*...Você sobreviveu por enquanto",
            color= discord.Color.green()
    )
            arquivo =discord.File("images/viveu.png", filename="viveu.png")
            embed.set_image(url="attachment://viveu.png")
            embed.set_footer(text=f"Executado por {ctx.author.name}")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed,file=arquivo)

    

bot.run(token)

