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
import json
import requests
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class setupv2(commands.Cog, name="Setup"):
     def __init__(self, client):
        self.client = client



     @commands.command()
     async def jf(self, ctx, city, country, region):
      response = requests.get(f"https://vip.timezonedb.com/v2.1/get-time-zone?key=U7UYC4ZKQ6NB&format=json&by=city&city={city}&country={country}&region={region}")
      timezone = response.json()['zones'][0]['zoneName']
      await ctx.send(timezone)

       












    
def setup(client):
    client.add_cog(setupv2(client))