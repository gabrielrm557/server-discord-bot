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
    @commands.cooldown(1,2, commands.BucketType.user)
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
                    await ctx.send("⚠️ Bot não possui permissão para dar timeout neste neste usuario ⚠️")

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
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=EmbedPadrao.erro(
                    ctx,
                    f"Espere {error.retry_after:.1f} segundos antes de usar a roleta novamente."
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
            user=member  # 👈 ESSA LINHA AQUI RESOLVE
        )

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