import asyncio
from typing import Optional

from discord.ext import commands
import discord
from discord.ext.commands import has_permissions
import datetime
from datetime import datetime
import utils



class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
      chnl = message.channel.id
      if not message.author.bot:
        embed=discord.Embed(title="**DELETED MESSAGE**", description="", color=0xdb0404)
        embed.add_field(name="Message Deleted",value=message.content, inline=False)
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name="Message Sender", value=message.author.mention, inline = False)
        embed.add_field(name="Where?", value='<#' + str(chnl) + '>',inline= False)
        embed.set_footer(text="User ID: {}".format(message.author.id))
        syslog_chan = discord.utils.get(message.guild.channels, name="message-logs")
        log_message = await syslog_chan.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before, role_after):

        if role_before.name == "jailed" and role_after.name != "jailed":
            syslog_chan = discord.utils.get(role_before.guild.channels, name="general")
            await syslog_chan.send("This is a nono please dont do this again")
            

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
         return
        em = discord.Embed(title="Media Logger", decription=f'[Jump to Message]({message.jump_url})', color=0x32a852)
        em.add_field(name="** **", value=f'[Jump to Message]({message.jump_url})')
        em.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        em.set_footer(text=f'User ID: {message.author.id}|')
        for message in message.attachments:
           if message.filename.endswith('.png') or message.filename.endswith('.jpeg') or message.filename.endswith('.gif') or message.filename.endswith('.jpg'):
               file = await message.to_file()
               syslog_chan = discord.utils.get(self.role_before.guild.channels, name="message-logs")
               if syslog_chan:
                  log_message = await syslog_chan.send(embed=em)
              
def setup(client):
    client.add_cog(Logging(client))