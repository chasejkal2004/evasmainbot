from datetime import datetime

import dateparser
import discord
import pytz
from pymongo import MongoClient
from discord.ext import commands
import asyncio
from ruamel.yaml import YAML
import os
import random
import aiohttp

import dload
from Systems.levelsys import levelling
import json
import requests
import wget

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class cmd(commands.Cog, name="Setup"):
     def __init__(self, client):
        self.client = client


     @commands.command()
     async def randomhex(self, ctx):
      random_number = random.randint(0,16777215)
      hex_number = str(hex(random_number))
      main = int(hex_number, 16)
      embed=discord.Embed(title=f"Color generated is {hex_number}",colour=main)
      await ctx.send(embed=embed)
       


     @commands.command()
     async def geturl(self,ctx, emoji: discord.PartialEmoji):
        url = emoji.url
        await dload.save(url)






    
def setup(client):
    client.add_cog(cmd(client))