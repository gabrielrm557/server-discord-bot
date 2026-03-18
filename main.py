import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
import os
from deep_translator import GoogleTranslator

load_dotenv()
token = os.getenv("TOKEN")

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
    latencia = round(bot.latency * 1000)

    if latencia <= 100:
        status = "Excelente 🟢"
        cor = discord.Color.green()

    elif latencia < 200:
        status = "Bom 🟡"
        cor = discord.Color.gold()

    else:
        status = "Ruim 🔴"
        cor = discord.Color.red()
        await ctx.send(embed=embed)
        print(latencia)
    embed = discord.Embed(
    title='🏓 Pong!',
    description=f'📡 Latência: {latencia}ms\n⚡ Status: {status}',
    color=cor
)
    await ctx.send (embed=embed)

@bot.command(aliases=["foto","f"])
async def avatar(ctx,member:discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=(f"🖼 Avatar de {member.name}")
        )
        embed.set_image(url = member.display_avatar.url)
        embed.set_footer(text=f"Executado por {ctx.author.name}")
        embed.color = member.color
        await ctx.send(embed=embed)
        if member == ctx.author:
            print(f"[AVATAR] servidor={ctx.guild.name} usuario={ctx.author.name} visualizou o proprio avatar {member.name}")
        else:            
            print(f"[AVATAR] servidor={ctx.guild.name} usuario={ctx.author.name} visualizou o avatar de {member.name}")

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Não consegui encontrar esse usuário. Use @ ou um nome/ID válido.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argumento inválido. Use @ ou um nome/ID válido.")
    print(f"[AVATAR] servidor={ctx.guild.name} usuario={ctx.author.name} erro : não encontrado usuario")

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
    embed = discord.Embed(
        title="📖 Comandos do Bot",
        description="💬 Use os comandos abaixo para interagir com o bot\n",
        color=discord.Color.blue()
    )

    embed.set_footer(text="Use $comando para executar • Desenvolvido por Gabriel")
    embed.add_field(
        name='📌 Utilidades',
        value='**$ping** - verifica se o bot está online\n'
              '**$avatar** [@usuário] - mostra o avatar de um usuário ou o seu\n'
              '**$cor** <cor> - altera a cor do seu nome (necessário cargos configurados no servidor)',
        inline=False
    )

    embed.add_field(
        name='🌍 Tradução',
        value='**$en** <texto> - traduz para Inglês\n'
              '**$es** <texto> - traduz para Espanhol\n'
              '**$pt** <texto> - traduz para Português',
        inline=False
    )

    embed.add_field(
        name='🎮 Diversão',
        value='**$roleta** - joga roleta russa (1/6 de chance de timeout)\n'
              '**$8ball** - responde uma pergunta aleatoriamente\n'
              '**$quem** <pergunta> - sorteia uma pessoa aleatória do servidor',
        inline=False
    )

    embed.add_field(
        name='📄 Outros',
        value='**$update** - mostra as últimas atualizações do bot',
        inline=False
    )

    await ctx.send(embed = embed)
@bot.command()
async def cor(ctx, cor: str):

    cores = {
    # vermelho
    "vermelho": "vermelho",
    "rojo": "vermelho",
    "red": "vermelho",

    # azul
    "azul": "azul",
    "blue": "azul",

    # verde
    "verde": "verde",
    "green": "verde",

    # roxo
    "roxo": "roxo",
    "morado": "roxo",
    "purple": "roxo",

    # rosa
    "rosa": "rosa",
    "pink": "rosa",

    # amarelo
    "amarelo": "amarelo",
    "amarillo": "amarelo",
    "yellow": "amarelo",

    # preto
    "preto": "preto",
    "negro": "preto",
    "black": "preto",

    # cinza
    "cinza": "cinza",
    "gris": "cinza",
    "gray": "cinza",
    "grey": "cinza",

    # branco
    "branco": "branco",
    "blanco": "branco",
    "white": "branco",

    # laranja
    "laranja": "laranja",
    "naranja": "laranja",
    "orange": "laranja",

    # marrom
    "marrom": "marrom",
    "marron": "marrom",
    "brown": "marrom",

    # ciano
    "ciano": "ciano",
    "cyan": "ciano"
}

    cor = cor.lower()
    cores_servidor = []
    for x in ctx.guild.roles:
        if x.name.lower() in cores:
            cores_servidor.append(x.name.lower())
    cores_servidor = list(set(cores_servidor))
    cores_servidor.sort()
    if cor in cores:
        cor_final = cores[cor]
        #cor não existe em cargos do servidor
        if cor_final not in cores_servidor:
                await ctx.send("❌ Essa cor não está disponível neste servidor.\n🎨 Cores disponíveis:\n" + "\n".join(cores_servidor))
                print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=falha_nao_configurado_no_servidor')
                return
    #cor invalida
    else:
        await ctx.send("❌ Não reconheci essa cor.\n 🎨 Cores disponíveis no servidor:\n" + "\n".join(cores_servidor))
        print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} input={cor} status=cor_invalida')
        return
    

    # remover cores antigas
    for role in ctx.author.roles:
        if role.name.lower() in cores_servidor:
            await ctx.author.remove_roles(role)

    # pegar cargo da nova cor
    role = discord.utils.get(ctx.guild.roles, name=cor_final)

    if role:
        try:
            await ctx.author.add_roles(role)
            await ctx.send(f"🎨 Sua cor agora é **{cor_final}**!")
            print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=sucesso')
        except discord.errors.Forbidden:
            await ctx.send("❌ Não consegui alterar sua cor.\nVerifique se meu cargo está acima dos cargos de cor e se tenho permissão para gerenciar cargos.")
            print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=falha_erro_permissao')
    else:
        await ctx.send("❌ Não encontrei esse cargo de cor no servidor.")
        print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=falha_nao_encontrado')

@bot.command()
async def quem(ctx, *, pergunta):
    membros = [m for m in ctx.guild.members if not m.bot]
    escolhido = random.choice(membros)

    await ctx.send(f"{pergunta}\n é : {escolhido.mention}")

@bot.command(aliases=["8ball"])
async def ball(ctx,*, pergunta:str = None):
    if pergunta is None or pergunta.strip() == "":
        await ctx.send("❌ Você precisa fazer uma pergunta!\nEx: $8ball vou ficar rico?")
        print(f'[8BALL] servidor={ctx.guild.name} usuario={ctx.author.name} status:erro pergunta_vazia')
        return
    lista = ['SIM','NÃO','TALVEZ']
    resultado = random.choice(lista)
    if resultado == "SIM":
        cor = discord.Color.green()
        desc = f"🔮 A resposta é...\n\n ✅ **{resultado}**"
    elif resultado == "NÃO":
        cor = discord.Color.red()
        desc = f"🔮 A resposta é...\n\n ❌ **{resultado}**"
    else:
        cor = discord.Color.purple()
        desc = f"🔮 A resposta é...\n\n 🤔 **{resultado}**"

    embed = discord.Embed(
        title="🎱 Magic 8 Ball",
        description=desc,
        color= cor
    )
    arquivo = discord.File("images/8ball.png", filename="8ball.png")
    embed.set_image(url="attachment://8ball.png")    
    embed.set_footer(text=f"Executado por {ctx.author.name}")
    await ctx.send(embed=embed,file=arquivo)

@bot.command()
async def update(ctx):
    with open("changelog.md", "r", encoding="utf-8") as f:
        conteudo = f.read()

    partes = conteudo.split("\n## V")

    bloco = "## V" + partes[1]

    if len(partes) > 2:
        bloco = bloco.split("\n## V")[0]

    embed = discord.Embed(
        title="📄 Última atualização",
        description=bloco[:4000]
    )

    await ctx.send(embed=embed)
@bot.command()
async def roleta(ctx):
    resultado = random.randint(1,6)
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

        print(f'[ROLETA] servidor={ctx.guild.name} usuario={ctx.author.name} resultado={resultado} status=morreu')

        try:
            await ctx.author.timeout(timedelta(seconds=30))
        except discord.errors.Forbidden:
            print(f'[ROLETA] servidor={ctx.guild.name} usuario={ctx.author.name} resultado={resultado} status=falha_erro_permissao')
            await ctx.send("⚠️ Bot não possui permissão para dar timeout neste neste usuario ⚠️")

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

        print(f'[ROLETA] servidor={ctx.guild.name} usuario={ctx.author.name} resultado={resultado} status=sobreviveu')

        await ctx.send(embed=embed,file=arquivo)


bot.run(token)

