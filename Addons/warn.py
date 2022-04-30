import dateparser
import discord
import pytz
import asyncio
from pymongo import MongoClient
from discord.ext import commands
from kumoslab.get import getXPColour
from ruamel.yaml import YAML
import os
import calendar
import string
import datetime
from discord.utils import get
import random
from nanoid import generate
from datetime import datetime
import pymongo
from pymongo import MongoClient
import paramiko
from Systems.levelsys import levelling
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


MONGODB_URI = os.getenv("MONGODB_URI")
COLLECTION = os.getenv("COLLECTION")
DB_NAME = os.getenv("WARNING_DATABASE")

# Please enter your mongodb details in the .env file.
cluster = MongoClient(MONGODB_URI)
warning = cluster[COLLECTION]["warnings"]


class warn(commands.Cog, name="Moderation"):
  def __init__(self, bot):
     self.bot = bot

  @commands.command()
  async def warn(self,ctx,member:discord.Member, reason):
    
    logs = generate(size=6)
    print(logs)
    ct = datetime.now()
    dt_string = ct.strftime("%d/%m/%Y %H:%M:%S")
    newuser = {"guildid": ctx.guild.id, "id": member.name + "#" + member.discriminator, "logid": logs, "time": dt_string,"moderator": ctx.author.name + "#" + ctx.author.discriminator,"reason": reason}
    warning.insert_one(newuser)
    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$push": {"warnid": logs}})
    student = []

    tbl = "<tr><td>LogID</td><td>Member</td><td>Moderator</td><td>Reason</td></tr>"
    student.append(tbl)

    for y in warning.find({"guildid": 938673742886867024}):
        a = "<tr><td>%s</td>"%y['logid']
        student.append(a)
        a2 = "<td>%s</td>"%y['id']
        student.append(a2)
        b = "<td>%s</td>"%y['moderator']
        student.append(b)
        c = "<td>%s</td></tr>"%y['reason']
        student.append(c)

    contents = f'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta content="text/html; charset=ISO-8859-1"
    http-equiv="content-type">
    <title>{ctx.guild.name}</title>
    </head>
    <body>
    <table>
    %s
    </table>
    </body>
    </html>
    '''%(student)

    filename = 'guildid.html'

    def main(contents, filename):
        output = open(filename,"w")
        output.write(contents)
        output.close()

    main(contents, filename)


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('173.201.190.131', username="t8wfy2zp5bn8", password="Kalbfell04")
    sftp = ssh.open_sftp()

    localpath = 'guildid.html'
    remotepath = 'public_html/guildid.html'
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()
    os.remove("guildid.html")
    print("Success.")
  @commands.command()
  async def warns(sled,ctx,member:discord.Member):
      stats = levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
      warns = stats["warnid"]
      embed=discord.Embed(title="User Warns")
      for x in warns:
        print(x)
        warnstats = warning.find_one({"guildid": ctx.guild.id, "id": member.id, "logid": x})
        time = warnstats["time"]
        reason = warnstats["reason"]
        moderator = warnstats["moderator"]
        log = warnstats["logid"]
        embed.add_field(name="Caselog ID: "+ log, value="Reason: "+ reason + "\nTime:" + time + "\nModerator:"+moderator, inline=False)
      await ctx.send(embed=embed)


  @commands.command()
  async def delwarn(self,ctx,member:discord.Member, x):

    warning.delete_one({"guildid": ctx.guild.id, "id": member.id, "logid": x})
    levelling.update_one({"guildid": ctx.guild.id, "id": member.id}, {"$pull": {"warnid": x}})
    print("Success.")



def setup(client):
    client.add_cog(warn(client))