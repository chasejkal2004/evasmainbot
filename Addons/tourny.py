from datetime import datetime

import dateparser
import discord
import pytz
import asyncio
from pymongo import MongoClient
from discord.ext import commands
from kumoslab.get import getXPColour
from ruamel.yaml import YAML
import os
from Systems.levelsys import levelling
from discord.utils import get
import random
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

class tourny(commands.Cog, name="Moderation"):
  def __init__(self, bot):
     self.bot = bot

  @commands.command()
  async def balls(self, ctx, playeramount):
    #people = random.sample(set(["chase", "alex", "shane", "emi", "icu", "swiftor"]), 6)
    #print(people[0] + " VS "+ people[1])
    #print(people[2] + " VS "+ people[3])
    #print(people[4] + " VS "+ people[5])
    #await ctx.send(people[0] + " VS "+ people[1])
    #await ctx.send(people[2] + " VS "+ people[3])
    #await ctx.send(people[4] + " VS "+ people[5])
    newgame = {"name": "base", "numofteams":playeramount}
    levelling.insert_one(newgame)

  @commands.command()
  async def addp(self, ctx, mcign):
      levelling.update_one({"name": "base"}, {"$push": {"players": mcign}})    

  @commands.command()
  async def bracket(self, ctx):
    stats = levelling.find_one({"name": "base"})
    await ctx.send("Current players in")
    people = stats["players"]
    await ctx.send(people[0]+ " " + people[1]+ " "+ people[2]+ " " + people[3]+" "+people[4]+ " " + people[5])
  @bracket.error
  async def bracket_error(self,ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Invalid amount of players contact chase to fix.')

  @commands.command()
  async def moveon(self, ctx, mcign,round):  
    levelling.update_one({"name": "base"}, {"$push": {f"round{round}": mcign}}) 
    await ctx.send(f"Moved on {mcign} to round{round}")

def setup(client):
    client.add_cog(tourny(client))