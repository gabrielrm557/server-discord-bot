from discord.ext import commands
import discord
from utils.embed import EmbedPadrao


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setchannel(self,ctx,channel: discord.TextChannel = None):

        if channel is None:
            await ctx.send("❌ Você precisa mencionar um canal.\nEx: $setchannel #comandos-nyx")
            return

        await ctx.send(f"Canal configurado: {channel.mention}")





async def setup(bot):
    await bot.add_cog(admin(bot))