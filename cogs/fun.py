from discord.ext import commands
import discord
import random
from datetime import timedelta
from utils.embed import EmbedPadrao
from database.roleta_db import DBroleta

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.user)
    async def roleta(self, ctx,member:discord.Member = None):
            user_id = ctx.author.id
            server_id = ctx.guild.id
            DBroleta.garantir_usuario(user_id,server_id)
            resultado = random.randint(1,6)
            morte = 1
            if resultado == morte:
                DBroleta.registrar_morte(user_id,server_id)
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
                    await ctx.send("⚠️ Bot não possui permissão para dar timeout neste usuario ⚠️")

                await ctx.send(embed=embed,file=arquivo)

            else:
                DBroleta.registrar_sobrevivencia(user_id,server_id)
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
            

    @roleta.error
    async def roleta_error(self, ctx, error):
        tempo = round(error.retry_after, 1)
        variacao_roleta = [
            f"⏳ Espere {tempo}s antes de usar a roleta novamente.",
            f"🎲 Calma aí... tente novamente em {tempo}s.",
            f"⌛ A roleta ainda está recarregando... aguarde {tempo}s.",
            f"🕒 Segura um pouco! Você poderá jogar novamente em {tempo}s.",
            f"⚠️ Muito rápido! Espere {tempo}s para tentar de novo."
            ]
        mensagem = random.choice(variacao_roleta).format(error=error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=EmbedPadrao.erro(
                    ctx,
                    mensagem
                )
            )

    @commands.command()
    async def rankroleta(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = member.id
        server_id = ctx.guild.id

        DBroleta.garantir_usuario(user_id, server_id)

        resultado = DBroleta.obter_stats(user_id, server_id)

        embed = EmbedPadrao.criar(
            ctx=ctx,
            title="🎲 Estatísticas da Roleta",
            description=(
                f"👤 {member.display_name}\n\n"
                f"🎯 Partidas: {resultado[0]}\n"
                f"☠️ Mortes: {resultado[1]}\n"
                f"✅ Sobreviveu: {resultado[2]}\n"
                f"🔥 Streak Atual: {resultado[3]}\n"
                f"🏆 Melhor Streak: {resultado[4]}"
            ),
            user=member  
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def toproleta(self,ctx):
        server_id = ctx.guild.id

        resultado_mortes = DBroleta.top_mortes(server_id)
        resultado_partidas = DBroleta.top_partidas(server_id)
        resultado_sobrevivencias = DBroleta.top_sobrevivencias(server_id)
        resultado_melhor_streak = DBroleta.top_streak(server_id)

        def formatar_top(resultado, sufixo):
            if not resultado:
                return "Nenhum dado ainda."

            medalhas = ["🥇", "🥈", "🥉", "🏅", "🏅"]
            linhas = []

            for i, (user_id, valor) in enumerate(resultado):
                member = ctx.guild.get_member(user_id)
                nome = member.display_name if member else f"ID {user_id}"
                linhas.append(f"{medalhas[i]} **{nome}** — `{valor}` {sufixo}")

            return "\n".join(linhas)

        embed = discord.Embed(
            title="🏆 Top Roleta do Servidor",
            description="Veja quem mais se destacou na roleta por aqui.",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="☠️ Mais mortes",
            value=formatar_top(resultado_mortes, "mortes"),
            inline=False
        )

        embed.add_field(
            name="🎯 Mais partidas",
            value=formatar_top(resultado_partidas, "partidas"),
            inline=False
        )

        embed.add_field(
            name="✅ Mais sobrevivências",
            value=formatar_top(resultado_sobrevivencias, "sobrevivências"),
            inline=False
        )

        embed.add_field(
            name="🔥 Melhor streak",
            value=formatar_top(resultado_melhor_streak, "de streak"),
            inline=False
        )

        embed.set_footer(text=f"Executado por {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball"])            
    async def ball(self,ctx,*, pergunta:str = None):
        if pergunta is None or pergunta.strip() == "":
            await ctx.send(embed=EmbedPadrao.erro(
                ctx,
                "Você precisa fazer uma pergunta.\n\nExemplo: `!8ball vou ficar rico?`"
            ))
            print(f'[8BALL] servidor={ctx.guild.name} usuario={ctx.author.name} status:erro pergunta_vazia')
            return

        lista = ['SIM','NÃO','TALVEZ']
        resultado = random.choice(lista)

        if resultado == "SIM":
            cor = discord.Color.green()
            emoji = "✅"
        elif resultado == "NÃO":
            cor = discord.Color.red()
            emoji = "❌"
        else:
            cor = discord.Color.purple()
            emoji = "🤔"

        desc = f"**{pergunta}**\n\n🔮 Resposta:\n{emoji} **{resultado}**"

        embed = discord.Embed(
            title="🎱 Magic 8 Ball",
            description=desc,
            color=cor
        )

        arquivo = discord.File("images/8ball.png", filename="8ball.png")
        embed.set_image(url="attachment://8ball.png")    
        embed.set_footer(text=f"Executado por {ctx.author.name}")

        await ctx.send(embed=embed,file=arquivo)

    @commands.command()
    async def quem(self,ctx, *, pergunta = None):
        if pergunta is None or pergunta.strip() == "": 
            await ctx.send(embed=EmbedPadrao.erro(
                ctx,
                "Você precisa fazer uma pergunta.\n\nExemplo: `!quem é o mais lindo do discord?`"
            ))
            print(f'[QUEM] servidor={ctx.guild.name} usuario={ctx.author.name} status=erro argumento_ausente')
            return

        membros = [m for m in ctx.guild.members if not m.bot]

        if not membros:
            await ctx.send(embed=EmbedPadrao.erro(
                ctx,
                "Não encontrei membros válidos para sortear."
            ))
            return

        escolhido = random.choice(membros)

        embed = discord.Embed(
            title="🎯 Quem?",
            description=f"**{pergunta}**\n\n👉 {escolhido.mention}",
            color=discord.Color.purple()
        )

        embed.set_footer(text=f"Executado por {ctx.author.name}")
        embed.set_thumbnail(url=escolhido.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))