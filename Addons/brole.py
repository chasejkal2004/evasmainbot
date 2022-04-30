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


class rolecmd(commands.Cog, name="Roles"):
     def __init__(self, bot):
        self.bot = bot
     @commands.group(invoke_without_command=True)
     async def brole(self, ctx):
        await ctx.send("Ping 1")
     @brole.command()
     async def create(self, ctx, role: str):
          levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"role": f"{role}"}})
          await ctx.send(f"Assigned {role} to be your booster role")
          guild = ctx.guild
          role2 = await guild.create_role(name=role)
          await ctx.author.add_roles(role2) 
     @brole.command()
     async def color(self, ctx, color):
        await ctx.send("did it work?")
        member = ctx.author
        data = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
        rolename = data["role"]
        if rolename == "":
          await ctx.send("You do not have a booster role. To create one do !brole create")
        role = discord.utils.get(member.guild.roles, name=rolename)
        color2 = color.replace("#","")
        main = int(color2, 16)
        await role.edit(colour=main)

     @brole.command()
     async def role(self, ctx, role:discord.Role):
        print(role.position)
        levelling.update_one({"server": ctx.guild.id}, {"$set": {"brolenum": f"{role.position}"}})

     @brole.command()
     async def rename(self, ctx, rname):
        member = ctx.author
        data = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})                                                                                                                                                                                                                                            
        rolename = data["role"]
        if rolename is None:
          return await ctx.send("You do not have a booster role. To create one do !brole create")
        role = discord.utils.get(member.guild.roles, name=rolename)
        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"role": f"{rname}"}})
        await role.edit(name=rname)
        await ctx.send(f"Succesfully renamed your role to `{rname}`")       
def setup(client):
    client.add_cog(rolecmd(client))