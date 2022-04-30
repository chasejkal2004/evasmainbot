[]
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
def print_diagonal_pairs(a):
    rows, cols = a.shape
    for row in range(rows):
        for col in range(cols):
            max_shift_amount = min(rows, cols) - min(row, col)
            for shift_amount in range(1, max_shift_amount+1):
                try:
                    print(a[row, col], a[row+shift_amount, col+shift_amount])
                except IndexError:
                    continue


class moderation(commands.Cog, name="Moderation"):
  def __init__(self, bot):
     self.bot = bot


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
  @commands.has_permissions(manage_messages=True)
  async def imute(self, ctx, member: discord.Member):
    await ctx.send(f"Took away {member.name} image perms")
    role = discord.utils.get(member.guild.roles, name="imuted")
    await member.add_roles(role)




  @commands.command()
  async def tempmute(self, ctx,member:discord.Member, timeInput=None,*,Reason=None):
    if timeInput is None:
      return
    try:
        try:
            time = int(timeInput)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            await asyncio.sleep(time)
            await ctx.send("It works")
    except:
        await ctx.send(f"Your reason is {timeInput}")
  
  @commands.command()
  async def jail(self, ctx,member:discord.Member,timeInput=None,*,Reason=None):
    if timeInput is None:
      return
    try:
        try:
            time = int(timeInput)
        except:
            role = discord.utils.get(member.guild.roles, name="jailed")
            await member.add_roles(role)
            await ctx.send("Jailed")
            await member.send
          
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            await asyncio.sleep(time)
            await member.remove_roles(role)
    except:
        await ctx.send(f"Your reason is {timeInput} {Reason}")


def setup(client):
    client.add_cog(moderation(client))