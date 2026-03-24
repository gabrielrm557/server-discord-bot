from discord.ext import commands
import discord
from utils.embed import EmbedPadrao
from database.config_db import DBConfig

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setchannel(self,ctx,*,off = None):
        server_id = ctx.guild.id
        prefix = DBConfig.get_prefix(server_id)
        if off is None:
            print(f"[SETCHANNEL] servidor={ctx.guild.name} usuario={ctx.author.name} status=erro argumento_ausente")
            await ctx.send(f"❌ Você precisa mencionar um canal.\nEx: {prefix}setchannel #comandos-nyx")
            return
        off = off.strip()
        
        
        if off.lower() == "off":
            if DBConfig.get_channel(server_id) is None:
                await ctx.send("Sem canal de comandos configurado.\n A Nyx ja responde em qualquer canal.")
                return
            else:
                DBConfig.remove_channel(server_id)
                print(f"[SETCHANNEL] servidor={ctx.guild.name} usuario={ctx.author.name} status=canal_removido")
                await ctx.send("Canal de comandos removido.\n Agora a Nyx responde em qualquer canal.")
                return
        
        try:
            channel = await commands.TextChannelConverter().convert(ctx,off)
            DBConfig.set_channel(server_id,channel.id)
            print(f"[SETCHANNEL] servidor={ctx.guild.name} usuario={ctx.author.name} canal_id={channel.id} canal_nome={channel.name} status=sucesso")
            await ctx.send(f"Canal configurado: {channel.mention}")
            return
        except:
            print(f"[SETCHANNEL] servidor={ctx.guild.name} usuario={ctx.author.name} input={off} status=canal_invalido")
            await ctx.send(f"❌ Você precisa mencionar um canal.\nEx: {prefix}setchannel #comandos-nyx")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self,ctx,*, prefix):
        server_id = ctx.guild.id
        prefix = prefix.strip()
        if prefix is None:
            print(f"[SETPREFIX] servidor={ctx.guild.name} usuario={ctx.author.name} status=erro prefixo_ausente")
            await ctx.send("❌ Você precisa informar um prefix valido.")
            return
        elif len(prefix) > 3:
            print(f"[SETPREFIX] servidor={ctx.guild.name} usuario={ctx.author.name} prefix={prefix} status=erro prefixo_muito_grande")
            await ctx.send("❌ Prefixo muito grande, tamanho maximo de 3 caracteres. ")
        else:
            DBConfig.set_prefix(server_id,prefix)
            print(f"[SETPREFIX] servidor={ctx.guild.name} usuario={ctx.author.name} prefix={prefix} status=sucesso")
            await ctx.send(f'Prefixo alterado para "{prefix}"')

    @commands.command()
    async def nyxconfig(self,ctx):
        server_id = ctx.guild.id
        prefix = DBConfig.get_prefix(server_id)
        channel = DBConfig.get_channel(server_id)
        if channel is None:
            print(f"[NYXCONFIG] servidor={ctx.guild.name} usuario={ctx.author.name} prefix={prefix} canal=nao_configurado")
            await ctx.send(f'Prefixo configurado : "{prefix}"\n Canal configurado : Não configurado')
            return

        print(f"[NYXCONFIG] servidor={ctx.guild.name} usuario={ctx.author.name} prefix={prefix} canal={channel}")
        await ctx.send(f'Prefixo configurado : "{prefix}"\n Canal configurado : <#{channel}>')

async def setup(bot):
    await bot.add_cog(Admin(bot))