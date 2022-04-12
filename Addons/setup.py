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


class setupv2(commands.Cog, name="Setup"):
  def __init__(self, client):
        self.client = client
  @commands.command()
  async def test2(self, ctx):
    await ctx.send("What is your muted role")

    def check1(m):
        return m.channel == ctx.channel and m.author == ctx.author
    role=await self.client.wait_for('message',check=check1)
    if role.content == 'cancel':
        await ctx.send("Cancel")
        return
    mutedrole_id = role.content.replace("<@&","").replace(">","")
    if mutedrole_id.isnumeric() == False:
      await ctx.send("Please make sure to ping the role.")
      return
    levelling.update_one({'server': ctx.guild.id}, {'$set': {'mutedRole': mutedrole_id}})
    await ctx.send("Would you like to setup modlogs? Yes or No.(Please use captial letters or your message will not go through.)")
    def check2(m):
        return m.channel == ctx.channel and m.author == ctx.author
    msg2 = await self.client.wait_for('message',check=check2)
    if msg2.content == 'Yes':
        await ctx.send("Awesome! What channel do you want your moderation actions to go to? This will include mutes, bans, warns, kicks")

        def check3(m):
          return m.channel == ctx.channel and m.author == ctx.author
        chan1 = await self.client.wait_for('message',check=check3)
        if chan1.content == 'cancel':
          await msg.edit(embed=embcancel, delete_after=10)
          return

        c = chan1.content[:-1]
        c2 = c[2:]
      
        chanob=self.client.get_channel(int(c2))
        await ctx.send(chanob.mention)
    if msg2.content == 'No':
      await ctx.send("Aight bitch")

def setup(client):
    client.add_cog(setupv2(client))