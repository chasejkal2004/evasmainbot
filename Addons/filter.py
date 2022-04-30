
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
MONGODB_URI = os.getenv("MONGODB_URI")
COLLECTION = os.getenv("COLLECTION")
DB_NAME = os.getenv("WARNING_DATABASE")

# Please enter your mongodb details in the .env file.
cluster = MongoClient(MONGODB_URI)
filter2 = cluster[COLLECTION]["filter"]

class filter(commands.Cog, name="Roles"):
     def __init__(self, bot):
        self.bot = bot
     @commands.group(invoke_without_command=True)
     async def filter(self, ctx):
        await ctx.send("Ping 1")
     @filter.command()
     async def add(self, ctx, word, whatitdo = None):
      if whatitdo in ["delete","ban","warn","delete","kick"]:
        
        stats = filter2.find_one({"guildid": ctx.guild.id, "word": word})
        if whatitdo == None:
          whatitdo = "delete"
        if whatitdo == "ban":
          whatitdo = "ban"
        if whatitdo == "warn":
          whatitdo = "warn"
        if whatitdo == "delete":
          whatitdo = "delete"
        if whatitdo == "kick":
          whatitdo = "kick"
          
        if stats is None: 
         print(f"im gay {whatitdo}")
         newuser = {"guildid": ctx.guild.id,"word": word, "moderator": ctx.author.name+ "#"+ ctx.author.discriminator, "punishment": whatitdo}
         filter2.insert_one(newuser)
         levelling.update_one({"server": ctx.guild.id}, {"$push": {"filterwords": word}})
        else:
          print("This is already in the filter. To check the filter please do !filter list")
      else:
        print("Invalid punishment. Please choose from delete, ban, warn, and kick. Thanks!")
     @filter.command()
     async def remove(self, ctx, word):
        filter2.delete_one({"guildid": ctx.guild.id, "word": word})
     @filter.command()
     async def removeall(self, ctx):
        filter2.delete_many({"guildid": ctx.guild.id})
     @filter.command()
     async def list(self, ctx):

      stats = levelling.find_one({"server": ctx.guild.id})
      warns = stats["filterwords"]
      if warns[50] is None:
        print("Balls")
      embed=discord.Embed(title="Filtered Words")
      embed2=discord.Embed(title="FIltered words 2")
      embed3=discord.Embed(title="FIltered words 3")
      embed4=discord.Embed(title="FIltered words 4")
      for x in warns:
        warnstats = filter2.find_one({"guildid": ctx.guild.id, "word": x})
        punishment = warnstats["punishment"]
        moderator = warnstats["moderator"]
        embed.add_field(name="Word: "+ x, value="Punishment: " + punishment + "\nModerator:"+moderator, inline=False)
        
        #await ctx.send("Hey there is to many filters to view them all do ")

      for x in warns[25:]:
        embed2.add_field(name="Word: "+ x, value="Punishment: " + punishment + "\nModerator:"+moderator, inline=False)
      for x in warns[50:]:
        embed3.add_field(name="Word: "+ x, value="Punishment: " + punishment + "\nModerator:"+moderator, inline=False)
      for x in warns[75:]:
        embed3.add_field(name="Word: "+ x, value="Punishment: " + punishment + "\nModerator:"+moderator, inline=False)
      for x in warns[100:]:
        embed4.add_field(name="Word: "+ x, value="Punishment: " + punishment + "\nModerator:"+moderator, inline=False)
      msg = await ctx.send(embed=embed)
      await msg.edit(embed=embed2)      
def setup(client):
    client.add_cog(filter(client))