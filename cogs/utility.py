from discord.ext import commands
import discord
from deep_translator import GoogleTranslator
from utils.embed import EmbedPadrao
from database.config_db import DBConfig



class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self,ctx):
        latencia = round(self.bot.latency * 1000)

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

        embed = EmbedPadrao.criar(
            ctx,
            title="🏓 Pong!",
            description=f"📡 Latência: {latencia}ms\n⚡ Status: {status}",
            color=cor
        )

        print(f"[PING] servidor={ctx.guild.name} usuario={ctx.author.name} latencia_ms={latencia} status={status}")

        await ctx.send(embed=embed)


    @commands.command(aliases=["es"])
    async def espanhol(self,ctx, *, texto):
        traducao = GoogleTranslator(source='auto', target="es").translate(texto)

        print(f"[TRADUCAO] servidor={ctx.guild.name} usuario={ctx.author.name} idioma=es")

        await ctx.send(traducao)


    @commands.command(aliases=["pt"])
    async def portugues(self,ctx, *, texto):
        traducao = GoogleTranslator(source='auto', target="pt").translate(texto)

        print(f"[TRADUCAO] servidor={ctx.guild.name} usuario={ctx.author.name} idioma=pt")

        await ctx.send(traducao)


    @commands.command(aliases=["en"])
    async def ingles(self,ctx, *, texto):
        traducao = GoogleTranslator(source='auto', target="en").translate(texto)

        print(f"[TRADUCAO] servidor={ctx.guild.name} usuario={ctx.author.name} idioma=en")

        await ctx.send(traducao)


    @commands.command(aliases=["foto","f"])
    async def avatar(self,ctx,member:discord.Member = None):
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
    async def avatar_error(self,ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Não consegui encontrar esse usuário. Use @ ou um nome/ID válido.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Argumento inválido. Use @ ou um nome/ID válido.")

        print(f"[AVATAR] servidor={ctx.guild.name} usuario={ctx.author.name} status=erro_usuario_nao_encontrado")


    @commands.command(aliases=["ayuda", "help"])
    async def ajuda(self,ctx):
        server_id = ctx.guild.id
        prefix = DBConfig.get_prefix(server_id)

        print(f"[AJUDA] servidor={ctx.guild.name} usuario={ctx.author.name} prefix={prefix}")

        embed = discord.Embed(
            title="📖 Comandos do Bot",
            description=f"💬 Use `{prefix}ajuda` ou `{prefix}help` para ver os comandos disponíveis\n",
            color=discord.Color.blue()
        )

        embed.set_footer(text=f"Use {prefix}comando para executar • Desenvolvido por Gabriel")

        embed.add_field(
            name='📌 Utilidades',
            value=f'**{prefix}ping** - verifica se o bot está online\n'
                  f'**{prefix}avatar** [@usuário] - mostra o avatar de um usuário ou o seu\n'
                  f'**{prefix}cor** <cor> - altera a cor do seu nome (necessário cargos configurados no servidor)',
            inline=False
        )

        embed.add_field(
            name='🌍 Tradução',
            value=f'**{prefix}en** <texto> - traduz para Inglês\n'
                  f'**{prefix}es** <texto> - traduz para Espanhol\n'
                  f'**{prefix}pt** <texto> - traduz para Português',
            inline=False
        )

        embed.add_field(
            name='🎮 Diversão',
            value=f'**{prefix}roleta** - joga roleta russa (1/6 de chance de timeout)\n'
                  f'**{prefix}rankroleta** - mostra suas estatísticas da roleta\n'
                  f'**{prefix}rankroleta @user** - ver stats de outra pessoa\n'
                  f'**{prefix}toproleta** - mostra os destaques da roleta no servidor\n'
                  f'**{prefix}8ball** - responde uma pergunta aleatoriamente\n'
                  f'**{prefix}quem** <pergunta> - sorteia uma pessoa aleatória do servidor',
            inline=False
        )

        embed.add_field(
            name='⚙️ Configuração do servidor',
            value=
                f'**{prefix}setprefix** <prefixo> - altera o prefixo do bot neste servidor\n'
                f'**{prefix}setchannel** <#canal> - define um canal específico para comandos\n'
                f'**{prefix}setchannel off** - remove o canal configurado\n'
                f'**{prefix}nyxconfig** - mostra as configurações atuais do servidor',
            inline=False
        )

        embed.add_field(
            name='📄 Outros',
            value=f'**{prefix}update** - mostra as últimas atualizações do bot',
            inline=False
        )

        await ctx.send(embed=embed)


    @commands.command()
    async def cor(self,ctx, cor: str = None):
        server_id = ctx.guild.id
        prefix = DBConfig.get_prefix(server_id)

        if cor is None or cor.strip() == "":
            await ctx.send(embed=EmbedPadrao.erro(ctx,f"Você precisa informar uma cor.\n\nExemplo: `{prefix}cor vermelho`"))
            print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} status=erro argumento_ausente')
            return

        cores = {
            "vermelho": "vermelho","rojo": "vermelho","red": "vermelho",
            "azul": "azul","blue": "azul",
            "verde": "verde","green": "verde",
            "roxo": "roxo","morado": "roxo","purple": "roxo",
            "rosa": "rosa","pink": "rosa",
            "amarelo": "amarelo","amarillo": "amarelo","yellow": "amarelo",
            "preto": "preto","negro": "preto","black": "preto",
            "cinza": "cinza","gris": "cinza","gray": "cinza","grey": "cinza",
            "branco": "branco","blanco": "branco","white": "branco",
            "laranja": "laranja","naranja": "laranja","orange": "laranja",
            "marrom": "marrom","marron": "marrom","brown": "marrom",
            "ciano": "ciano","cyan": "ciano"
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

            if cor_final not in cores_servidor:
                await ctx.send(embed=EmbedPadrao.erro(ctx,"Essa cor não está disponível neste servidor.\n\n🎨 **Cores disponíveis:**\n" + "\n".join(cores_servidor)))
                print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=falha_nao_configurado_no_servidor')
                return

        else:
            await ctx.send(embed=EmbedPadrao.erro(ctx,"Não reconheci essa cor.\n\n🎨 **Cores disponíveis no servidor:**\n" + "\n".join(cores_servidor)))
            print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} input={cor} status=cor_invalida')
            return

        for role in ctx.author.roles:
            if role.name.lower() in cores_servidor:
                await ctx.author.remove_roles(role)

        role = discord.utils.get(ctx.guild.roles, name=cor_final)

        if role:
            try:
                await ctx.author.add_roles(role)
                await ctx.send(embed=EmbedPadrao.sucesso(ctx,f"Sua cor agora é **{cor_final}**."))
                print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=sucesso')

            except discord.errors.Forbidden:
                await ctx.send(embed=EmbedPadrao.erro(ctx,"Não consegui alterar sua cor.\n\nVerifique se meu cargo está acima dos cargos de cor e se tenho permissão para gerenciar cargos."))
                print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=falha_erro_permissao')

        else:
            await ctx.send(embed=EmbedPadrao.erro(ctx,"Não encontrei esse cargo de cor no servidor."))
            print(f'[COR] servidor={ctx.guild.name} usuario={ctx.author.name} cor={cor_final} status=falha_nao_encontrado')


    @commands.command()
    async def update(self,ctx):

        print(f"[UPDATE] servidor={ctx.guild.name} usuario={ctx.author.name}")

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



async def setup(bot):
    await bot.add_cog(utility(bot))