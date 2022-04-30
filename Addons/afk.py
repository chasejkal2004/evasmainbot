from datetime import datetime

import dateparser
import discord
import pytz
from pymongo import MongoClient
from discord.ext import commands
import asyncio
from ruamel.yaml import YAML
import os
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class afk(commands.Cog, name="AFK"):
  def __init__(self, bot):
        self.bot = bot
  @commands.command()
  async def afk(self,ctx, *, reason=None):
    embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ffff)
    embed.set_footer(text=ctx.guild)
    if reason == None:
        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"AFK": "True"}})
        embed.add_field(name=f"{ctx.author.name} is now AFK", value="Reason: No reason specified.")
        await ctx.send(embed=embed)
    else:
        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"AFK": "True"}})
        embed.add_field(name=f"{ctx.author.name} is now AFK", value=f"Reason: {reason}", inline=False)
        await ctx.send(embed=embed)



  @commands.Cog.listener()
  async def on_message(self,message):
    if message.content.startswith('!afk'):
        return
    if message.author.bot: return
    stats = levelling.find_one({"guildid": message.guild.id, "id": message.author.id})
    if stats["AFK"] == "False":
        return
    if stats["AFK"] == "":
        return
    elif stats["AFK"] == "True":
        levelling.update_one({"guildid": message.guild.id, "id": message.author.id}, {"$set": {"AFK": "False"}})
        await message.channel.send("Dumbass returned from being afk") 
        return
    if message.mentions:
        memberm = levelling.find_one({"guildid": message.guild.id, "id": message.mentions[0].id})
        if memberm["AFK"] == "True":
          await message.channel.send("That person is currently afk")
def setup(client):
    client.add_cog(afk(client))