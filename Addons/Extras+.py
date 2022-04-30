# EXTRAS VERSION 1.0.0
import os

import discord
from discord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

class Extras(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Add-XP Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addxp(self, ctx, xpamount: int = None, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        if xpamount is None:
            embed2 = discord.Embed(description=":x: Please make sure you entered an integer.")
            await ctx.send(embed=embed2)
            return
        if xpamount < 0:
            embed3 = discord.Embed(description=":x: Please make sure you entered a positive integer.")
            await ctx.send(embed=embed3)
            return
        levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
        levelling.update_one({"guildid": ctx.guild.id, "id": member.id}, {"$inc": {"xp": xpamount}})
        embed4 = discord.Embed(title=":white_check_mark: Added XP!", description=f"Added `{xpamount}xp` to {member.mention}")
        await ctx.send(embed=embed4)
        return


    # REMOVE-XP COMMAND
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removexp(self, ctx, xpamount: int = None, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        if xpamount is None:
            embed2 = discord.Embed(description=":x: Please make sure you entered an integer.")
            await ctx.send(embed=embed2)
            return
        if xpamount < 0:
            embed3 = discord.Embed(description=":x: Please make sure you entered a positive integer.")
            await ctx.send(embed=embed3)
            return
        levelling.find_one({"guildid": ctx.guild.id, "id": member.id})
        levelling.update_one({"guildid": ctx.guild.id, "id": member.id}, {"$inc": {"xp": - xpamount}})
        embed4 = discord.Embed(title=":white_check_mark: Removed XP!", description=f"Removed `{xpamount}xp` from {member.mention}")
        await ctx.send(embed=embed4)
        return



    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def reset(self, ctx, member: discord.Member = None):
        if member:
            if not member.bot:
                levelling.update({"guildid": ctx.guild.id, "id": member.id},
                                 {"$set": {"rank": 1, "xp": 0}})
                embed = discord.Embed(title=f":white_check_mark: RESET USER", description=f"Reset User: {member.mention}",
                                      colour=config['success_embed_colour'])
                print(f"{member} was reset!")
                await ctx.send(embed=embed)
            else:
                prefix = config['Prefix']
                embed2 = discord.Embed(
                                       description=f"You cannot reset bots!",
                                       colour=config['error_embed_colour'])
                embed2.add_field(name="Example:", value=f"`{prefix}reset` {ctx.message.author.mention}")
                print("Resetting Failed. A user was either not declared or doesn't exist!")
                await ctx.send(embed=embed2)


# Sets-up the cog for Extras
def setup(client):
    client.add_cog(Extras(client))
