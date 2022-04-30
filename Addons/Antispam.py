import asyncio
import datetime
import os

import discord
from discord.ext import commands, tasks
from ruamel.yaml import YAML
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class Antispam(commands.Cog):
    def __init__(self, client):
        self.client = client

    # on ready event and check for if members have field message_count and if not add 0 to it, else continue
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            for member in self.client.get_all_members():
                if not member.bot:
                    check = levelling.find_one({'id': member.id, 'guildid': guild.id, 'message_count': {'$exists': True}})
                    if check:
                        levelling.update_one({'id': member.id, 'guildid': guild.id}, {'$set': {'message_count': 0}})
                        continue
                    else:
                        levelling.update_one({'id': member.id, 'guildid': guild.id}, {'$set': {'message_count': 0}})
                        print(f"[Anti-Spam] User {member.mention} was missing MESSAGE_COUNT - Automatically adding it!")



    # on message event that adds 1 to the message_count field of the user
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        # check if user has the ignored role
        server = levelling.find_one({'server': message.guild.id})
        ignored_role = discord.utils.get(message.guild.roles, name=server['ignoredRole'])
        if ignored_role in message.author.roles:
            return



        # Check if the user has a message_count field
        check = levelling.find_one({'id': message.author.id, 'guildid': message.guild.id, 'message_count': {'$exists': True}})
        if check:
            levelling.update_one({'id': message.author.id, 'guildid': message.guild.id}, {'$inc': {'message_count': 1}})
        else:
            levelling.update_one({'id': message.author.id, 'guildid': message.guild.id}, {'$set': {'message_count': 1}})
            #print(f'[Anti-Spam] User {message.mention} was missing MESSAGE_COUNT - Automatically adding it!')

        # check if message count is higher than warningMessages
        check = levelling.find_one(
            {'id': message.author.id, 'guildid': message.guild.id, 'message_count': {'$exists': True}})
        server = levelling.find_one({'server': message.guild.id})
        if check['message_count'] == server['warningMessages'] and check['message_count'] < server['muteMessages']:
            # dm the user
            await message.author.send(f"⚠️// You have been warned for spamming in `{message.guild}`!")
            # add 1 to the warnings field
            levelling.update_one({'id': message.author.id, 'guildid': message.guild.id}, {'$inc': {'warnings': 1}})
        elif check['message_count'] == server['muteMessages']:
            # dm the user
            await message.author.send(f"🔇️ // You have been muted for spamming in `{message.guild}`!")
            # add 1 to the warnings field
            levelling.update_one({'id': message.author.id, 'guildid': message.guild.id}, {'$inc': {'warnings': 1}})

            # create a role called "Muted" and add the user to it
            role = discord.utils.get(message.guild.roles, name="Muted")
            if not role:
                role = await message.guild.create_role(name="Muted")
                for channel in message.guild.text_channels:
                    await channel.set_permissions(role, send_messages=False)

            await message.author.add_roles(role)

            # check if the user has a mute_time field
            check = levelling.find_one({'id': message.author.id, 'guildid': message.guild.id, 'mute_time': {'$exists': True}})
            if check:
                # if the user has a mute_time field, set the time of mute to the current time
                levelling.update_one({'id': message.author.id, 'guildid': message.guild.id}, {'$set': {'mute_time': message.created_at}})
            else:
                # if the user doesn't have a mute_time field, create one and set the time of mute to the current time
                levelling.update_one({'id': message.author.id, 'guildid': message.guild.id}, {'$set': {'mute_time': message.created_at}})


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutetime(self, ctx, time: int = None):
        if time is None:
            embed = discord.Embed(title="🔇️ // Mute Time", description="Please enter a time in seconds!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if time < 0:
            embed = discord.Embed(title="🔇️ // Mute Time", description="Please enter a time in seconds!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if time > 0:
            levelling.update_one({'server': ctx.guild.id}, {'$set': {'mutedTime': time}})
            embed = discord.Embed(title="🔇️ // Mute Time", description=f"Mute time set to `{time}` seconds!", color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warningmessages(self, ctx, messages: int = None):
        if messages is None:
            embed = discord.Embed(title="⚠️ // Warning Messages", description="Please enter a number of messages!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if messages < 0:
            embed = discord.Embed(title="⚠️ // Warning Messages", description="Please enter a number of messages!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if messages > 0:
            levelling.update_one({'server': ctx.guild.id}, {'$set': {'warningMessages': messages}})
            embed = discord.Embed(title="⚠️ // Warning Messages", description=f"Warning messages set to `{messages}`!", color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutemessages(self, ctx, messages: int = None):
        if messages is None:
            embed = discord.Embed(title="🔇️ // Mute Messages", description="Please enter a number of messages!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if messages < 0:
            embed = discord.Embed(title="🔇️ // Mute Messages", description="Please enter a number of messages!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if messages > 0:
            levelling.update_one({'server': ctx.guild.id}, {'$set': {'muteMessages': messages}})
            embed = discord.Embed(title="🔇️ // Mute Messages", description=f"Mute messages set to `{messages}`!", color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ignoredrole(self, ctx, role: discord.Role = None):
        if role is None:
            embed = discord.Embed(title="⚠️ // Ignored Role", description="Please enter a role!", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        if role is not None:
            
            embed = discord.Embed(title="⚠️ // Ignored Role", description=f"Ignored role set to `{role.name}`!", color=0xFF0000)
            await ctx.send(embed=embed)
            return






def setup(client):
    client.add_cog(Antispam(client))

    # every 10 seconds it clears everyones message_count field
    @tasks.loop(seconds=10)
    async def clear_message_count():
        for guild in client.guilds:
            for member in guild.members:
                if not member.bot:
                    levelling.update_one({'id': member.id, 'guildid': guild.id}, {'$set': {'message_count': 0}})


    clear_message_count.start()

    # a task that checks every minute if the mute_time field is older than the time specified as muteTime
    @tasks.loop(seconds=10)
    async def unmute():
        for guild in client.guilds:
            for member in guild.members:
                if not member.bot:
                    check = levelling.find_one({'id': member.id, 'guildid': guild.id, 'mute_time': {'$exists': True}})
                    user = levelling.find_one({'id': member.id, 'guildid': guild.id})
                    server = levelling.find_one({'server': guild.id})
                    if check:
                        if user['mute_time'] < datetime.datetime.now() - datetime.timedelta(seconds=int(server['mutedTime'])):
                            # remove the mute role
                            role = discord.utils.get(guild.roles, name="Muted")
                            await member.remove_roles(role)
                            # remove the mute_time field
                            levelling.update_one({'id': member.id, 'guildid': guild.id}, {'$unset': {'mute_time': ""}})
                            # send a message to the user
                            await member.send(f"🔊 // You have been unmuted in `{guild}`!")
                    if not check:
                        continue




    unmute.start()
