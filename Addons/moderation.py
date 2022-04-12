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

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)



class moderation(commands.Cog, name="Moderation"):
  def __init__(self, bot):
     self.bot = bot
  @commands.command()
  async def warn(self,ctx, member: discord.Member, *,reason=None):
    levelling.update_one({"guildid": ctx.guild.id, "id": member.id}, {"$push": {"warns": reason+ " Warned by: "+ ctx.author.name + "#"+ctx.author.discriminator}})
    await ctx.send("Warned that MF")



  @commands.command()
  async def warnings(self, ctx, member:discord.Member):
        stats = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
        balls = (str(stats['warns']).replace('[', '').replace(']', ''))
        s = balls.replace("'","")
        main = s.replace(",","\n")
        rmain = stats['warns']
        print(rmain[0])
        embed=discord.Embed(title="Warning List", description="** **"+ main)
        embed2=discord.Embed(title="Warning List", description=main)
        await ctx.send(embed=embed)


  @commands.command()
  async def delwarn(self, ctx, member:discord.Member, warn):
        stats = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
        
        rmain = stats['warns']
        print(warn)
        print(rmain[int(warn)])
        shit = rmain[int(warn)]
        if rmain[int(warn)] in stats['warns']:
            levelling.update_one({"guildid": ctx.guild.id, "id": member.id},  {"$pull": {"warns": shit}})
            embed=discord.Embed(title="Warning List", description=f"Removed warn\n{rmain[int(warn)]}")
            await ctx.send(embed=embed)
        
  @delwarn.error
  async def delwarn_error(self,ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Invalid warn. Please make sure to only use numbers. Aswell as to start from 0.")
  @commands.command()
  async def mute(self,ctx,member:discord.Member, *,reason=None):
    if member is None:
      await ctx.send("Please provide a member.")
    if reason is None:
        reason = "No reason provided."
    await ctx.send(f"Muted {member.name} for {reason}.")
    

  @mute.error
  async def mute_error(self,ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('**You do not have manage_messages permssion!**')



  @commands.command()
  async def timer(self, ctx, member:discord.Member, timeInput):
    try:
        try:
            time = int(timeInput)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
        await member.add_role("balls")
    except:
        await ctx.send("Invalid time.")
def setup(client):
    client.add_cog(moderation(client))