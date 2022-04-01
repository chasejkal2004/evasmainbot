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

    # Help Command
    @commands.command(aliases=["h", "lh"])
    @commands.guild_only()
    async def help(self, ctx, helptype=None):
        if config['help_command'] is True:
            prefix = config['Prefix']
            top = config['leaderboard_amount']
            embed = discord.Embed(title=f"{self.client.user.name} Command List")
            if helptype is None:
                embed.add_field(name=f":camera: Profile",
                                value=f'`{prefix}help profile`\n[Hover for info](https://www. "Customise your rank cards background, xp colour and your profile pictures shape!")')
                embed.add_field(name=f":smile: Fun",
                                value=f"`{prefix}help fun`\n[Hover for info](https://www. 'Check yours or another persons rank card, or check out the leaderboard')")
                if os.path.exists("Addons/Clan System.py") is True:
                    embed.add_field(name=f"👥 Clans", value=f"`{prefix}help clans`\n[Hover for info](https://www. 'Get all commands for the clan system')")
                embed.set_footer(text="If you're on mobile, the hover button will not work")
                if ctx.author.id == config['bot_owner_id']:
                    embed.add_field(name=f":gear: Config",
                                    value=f"`{prefix}help config`\n[Hover for info](https://www. 'Customise the bot to your liking for your server!')")
                    embed.add_field(name=f":octagonal_sign: Admin",
                                    value=f"`{prefix}help admin`\n[Hover for info](https://www. 'Perform Admin commands on users, such as resetting')")
                elif ctx.message.author.guild_permissions.administrator:
                    embed.add_field(name=f":gear: Config",
                                    value=f"`{prefix}help config`\n[Hover for info](https://www. 'Customise the bot to your liking for your server!')")
                    embed.add_field(name=f":octagonal_sign: Admin",
                                    value=f"`{prefix}help admin`\n[Hover for info](https://www. 'Perform Admin commands on users, such as resetting')")
                await ctx.send(embed=embed)
            if helptype.lower() == "profile":
                embed = discord.Embed(title=f":camera: Profile Commands",
                                      description="```background, circlepic, xpcolour```")
                embed.add_field(name="Examples",
                                value=f"```🖼️ {prefix}background <link> -  Set your background using a Link (Imgur is "
                                      f"Recommended)\n⭕ {prefix}circlepic <True|False> - Sets the shape of your "
                                      f"Profile Picture\n🎨 {prefix}xpcolour <hex> - Changes your XP progress bar's "
                                      f"colour```")
                await ctx.send(embed=embed)
            elif helptype.lower() == "fun":
                embed = discord.Embed(title=f":smile: Fun Commands",
                                      description="```rank, leaderboard```")
                embed.add_field(name="Examples",
                                value=f"```📈 rank [user] - Displays the users current Level and XP Progress\n📊 "
                                      f"leaderboard [global] - Displays top {top} users in the server or the global "
                                      f"rankings```")
                await ctx.send(embed=embed)
            elif helptype.lower() == "admin":
                if ctx.message.author.guild_permissions.administrator:
                    embed = discord.Embed(title=f":octagonal_sign: Admin Commands",
                                          description="```reset, addxp, removexp```")
                    embed.add_field(name="Examples",
                                    value=f"```🔄 {prefix}reset <user> - Fully resets the user\n🤲 {prefix}addxp "
                                          f"<amount> <user> - Grants the user with XP\n❌ {prefix}removexp <amount> "
                                          f"<user> - Removes XP from the user```")
                    await ctx.send(embed=embed)
            elif helptype.lower() == "config":
                if ctx.message.author.guild_permissions.administrator:
                    embed = discord.Embed(title=f":gear: Config Commands",
                                          description="```antispam, doublexp, ignoredrole, levelchannel, mutedrole, "
                                                      "mutemessages, mutetime, role, warningmessages, xppermessage```")
                    embed.add_field(name="Examples",
                                    value=f"```❗ {prefix}doublexp <role> - Sets a role to earn x2 XP"
                                          f"\n📺 {prefix}levelchannel <channelName> - The channel where level "
                                          f"up messages get sent to\n"
                                          f"📜 {prefix}role <add|remove> <level> <rolename> - The role a user gets when "
                                          f"they reach a certain level\n💬 {prefix}xppermessage "
                                          f"<int> - The amount of xp you earn per message```")
                    await ctx.send(embed=embed)
            elif helptype.lower() == "clans":
                embed = discord.Embed(title=f"👥 Clan Commands",
                                      description="```join, delete, invite, leave, status, clan, clans, create```")
                embed.add_field(name="Examples",
                                value=f"```🔗 {prefix}join <clanName> - Joins a clan (If Public)"
                                      f"\n🗑️ {prefix}delete - Deletes your clan "
                                      f"(Must be the Owner)\n"
                                      f"✉️ {prefix}invite <@user> - Invites a user to the "
                                      f"clan\n👋 {prefix}leave"
                                      f"- Leaves the current clan you are in (Only Members Can)\n🟢 {prefix}status - "
                                      f"Makes your clan either Public or Private\n👤 {prefix}clan <clanName> - "
                                      f"Displays information about the specified clan\n👥 {prefix}clans - Displays 10 "
                                      f"Public Clans\n🆕 {prefix}create <clanName> <public|private> - Creates a Clan "
                                      f"that is either Public or Private```")
                await ctx.send(embed=embed)

# Sets-up the cog for Extras
def setup(client):
    client.add_cog(Extras(client))
