
from datetime import datetime

import dateparser
import discord
import pytz
from pymongo import MongoClient
from discord.ext import commands
from kumoslab.get import getXPColour
from ruamel.yaml import YAML
import os
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class fnick(commands.Cog, name="Roles"):
     def __init__(self, bot):
        self.bot = bot
     @commands.command()
     async def fn(self, ctx, member: discord.Member, nick):
       levelling.update_one({"guildid": ctx.guild.id, "id": member.id}, {"$set": {"nick": f"{nick}"}})
       await ctx.send(f"Set {member.name} nickname to {nick}")
       await member.edit(nick=nick)



       
     @commands.Cog.listener()
     async def on_member_update(self,before,after):
       stats = levelling.find_one({"guildid": after.guild.id, "id": after.id})
       nick2 = stats["nick"]
       if nick2 is None:
         return
       else:
         await after.edit(nick=nick2)
       
def setup(client):
    client.add_cog(fnick(client))