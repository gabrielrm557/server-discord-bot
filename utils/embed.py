import discord

class EmbedPadrao:
    @staticmethod
    def criar(ctx, title=None, description=None,user=None, color=discord.Color.blue()):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        embed.set_footer(text=f"Executado por {ctx.author.name}")

        if user is None:
            user = ctx.author

        embed.set_thumbnail(url=user.display_avatar.url)


        return embed
    
    @staticmethod
    def erro(ctx, mensagem):
        embed = discord.Embed(
            title="❌ Erro",
            description=mensagem,
            color=discord.Color.red()
        )

        embed.set_footer(text=f"Executado por {ctx.author.name}")

        return embed


    @staticmethod
    def sucesso(ctx, mensagem):
        embed = discord.Embed(
            title="✅ Sucesso",
            description=mensagem,
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Executado por {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        return embed


    @staticmethod
    def info(ctx, mensagem):
        embed = discord.Embed(
            title="ℹ️ Informação",
            description=mensagem,
            color=discord.Color.blue()
        )

        embed.set_footer(text=f"Executado por {ctx.author.name}")


        return embed
    