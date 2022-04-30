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
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class setupv2(commands.Cog, name="Setup"):
  def __init__(self, client):
        self.client = client
  @commands.command()
  async def msetup(self, ctx):
    jail =  await ctx.guild.create_text_channel("jail")
    jaillog = await ctx.guild.create_text_channel("jail-logs")
    jailrole = await ctx.guild.create_role(name="jailed")
    imuted = await ctx.guild.create_role(name="imuted")
    rmuted = await ctx.guild.create_role(name="rmuted")
    modlogs = await ctx.guild.create_text_channel("modlogs-logs")
    serverlogs = await ctx.guild.create_text_channel("server-logs")
    memberlogs = await ctx.guild.create_text_channel("member-logs")
    messagelogs = await ctx.guild.create_text_channel("message-logs")
    medialogs = await ctx.guild.create_text_channel("media-logs")
    joinleave = await ctx.guild.create_text_channel("join-leave-logs")
    voiceleave = await ctx.guild.create_text_channel("voice-logs")
    for channel in ctx.guild.channels:
          await channel.set_permissions(jailrole, send_messages=False, read_messages=True, read_message_history=True)
          await channel.set_permissions(rmuted, add_reactions=False)
          await channel.set_permissions(imuted, attach_files=False, embed_links=False)
    
    levelling.update_one({"server": ctx.guild.id}, {"$push": {"jail": jail.name, "jaillog": jaillog.name, "modlogs": modlogs.name, "memberlogs": memberlogs.name, "serverlogs": serverlogs.name, "messagelogs": messagelogs.name, "medialogs": medialogs.name, "joinleave": joinleave.name, "voiceleave": voiceleave.name}})


  @commands.group(invoke_without_command=True)
  async def config(self, ctx):
        await ctx.send("Bout to be hell.")
  @config.command()
  async def bandm(self, ctx,*, bandm):
      levelling.update_one({"server": ctx.guild.id}, {"$set": {"bandm": bandm}})
      e = discord.Embed(description=f"✅| Updated the ban direct message to {bandm}",color=0X00FF00)
      await ctx.send(embed=e)
  @config.command()
  async def warndm(self, ctx,*, warndm):
      levelling.update_one({"server": ctx.guild.id}, {"$set": {"warndm": warndm}})
      e = discord.Embed(description=f"✅| Updated the warn direct message to {warndm}.",color=0X00FF00)
      await ctx.send(embed=e)
  @config.command()
  async def jaildm(self, ctx,*, jaildm):
      levelling.update_one({"server": ctx.guild.id}, {"$set": {"jaildm": jaildm}})
      e = discord.Embed(description=f"✅| Updated the jail direct message to {jaildm}",color=0X00FF00)
      await ctx.send(embed=e)
  @config.command()
  async def staff(self, ctx, role:discord.Role):

        stats = levelling.find_one({"server": ctx.guild.id,})
        rmain = stats['staffrole']
        if role.name in rmain:
              await ctx.send("This is already a staff rank.")
              return
        else:
          e = discord.Embed(description=f"✅| Added **{role.name}** to the staff roles.",color=0X00FF00)
          await ctx.send(embed=e)
          levelling.update_one({"server": ctx.guild.id}, {"$push": {"staffrole": role.name}})
  @config.command()
  async def rolecheck(self, ctx):
        stats = levelling.find_one({"server": ctx.guild.id,})
        rmain = stats['staffrole']
        for role in ctx.author.roles:
              if role.name in rmain:
                 await ctx.send("Authorized.")
                 return














    
def setup(client):
    client.add_cog(setupv2(client))