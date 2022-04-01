from datetime import datetime

import dateparser
import discord
import pytz
from pymongo import MongoClient
from discord.ext import commands

from ruamel.yaml import YAML
import os
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


class TimezoneCommands(commands.Cog, name="Timezones"):
     def __init__(self, bot):
        self.bot = bot
     @commands.group(invoke_without_command=True)
     async def timezone(self, ctx):
        await ctx.send("Ping 1")
     @timezone.command()
     async def get(self, ctx, member: discord.Member = None):
       if member ==None:
          member = ctx.author
       stats = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
       tzname = stats["timezone"]
       tz = pytz.timezone(tzname)
       tz_now = datetime.now(tz)
       fmt = "%B %d, %I:%M %p"
       embed=discord.Embed(title="",description=f"<@{member.id}> current time is {tz_now.strftime(fmt)}")
       await ctx.send(embed=embed)
     @timezone.command()
     async def set(self, ctx, tzname: str):
        if tzname not in pytz.all_timezones:
            prefix = config['Prefix']
            embed=discord.Embed(title="Invalid Timezone.", color=0x00ff40)
            embed.add_field(name="** **", value=f"Must be properly capitalized ex: US/Eastern, Asia/Kolkata etc\nIf you need a list of timezone please use {prefix}timezones list", inline=True)
            return await ctx.send(embed=embed)
          
        if tzname in pytz.all_timezones:
            #levelling.update_one({"memberid": ctx.author.id, "tzname": tzname})
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"timezone": f"{tzname}"}})
            await ctx.send(f"Assigned timezone: {tzname}")


def setup(client):
    client.add_cog(TimezoneCommands(client))