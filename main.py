orialis
/
discord.pyimport discord
from discord.ext import commands
import os
from os import listdir
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole, NoPrivateMessage
from ruamel.yaml import YAML
import logging
import requests
from dotenv import load_dotenv
from discord import Webhook, RequestsWebhookAdapter
from Systems.levelsys import levelling
from instagramy import InstagramUser
import asyncio
load_dotenv()


#https://codingstatus.com/fetch-data-from-mongodb-using-mongoose/
# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless having issues with ruamel)
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Command Prefix + Removes the default discord.py help command
client = commands.Bot(command_prefix=commands.when_mentioned_or(config['Prefix']), intents=discord.Intents.all(), case_insensitive=True)


# sends discord logging files which could potentially be useful for catching errors.
os.remove("Logs/logs.txt")
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'
logging.basicConfig(filename='Logs/logs.txt', level=logging.DEBUG, format=FORMAT)
logging.debug('Started Logging')
logging.info('Connecting to Discord.')


@client.event  # On Bot Startup, Will send some details about the bot and sets it's activity and status. Feel free to remove the print messages, but keep everything else.
async def on_ready():
    config_status = config['bot_status_text']
    config_activity = config['bot_activity']
    activity = discord.Game(name=config['bot_status_text'])
    logging.info('Getting Bot Activity from Config')
    print("If you encounter any bugs, please let me know.")
    print('------')
    print('Logged In As:')
    print(f"Username: {client.user.name}\nID: {client.user.id}")
    print('------')
    print(f"Status: {config_status}\nActivity: {config_activity}")
    print('------')
    await client.change_presence(status=config_activity, activity=activity)
    for guild in client.guilds:
        serverstats = levelling.find({"server": guild.id, "role": {"$exists": False}})
        for doc in serverstats:
            levelling.update_one({"server": guild.id}, {"$set": {"role": [], "level": []}})
            print(f"Guild: {guild.name} was missing 'ROLE' and 'LEVEL' -  Automatically added it!")
        userstats = levelling.find({"guildid": guild.id, "name": {"$exists": False}, "id": {"$exists": True}})
        for doc in userstats:
            member = await client.fetch_user(doc["id"])
            levelling.update_one({"guildid": guild.id, "id": doc['id']}, {"$set": {"name": str(f"{member}")}})
            print(f"The field NAME was missing for: {member} - Automatically added it!")
    stats = levelling.find_one({"bot_name": f"{client.user.name}"})
    if stats is None:
        bot_data = {"bot_name": f"{client.user.name}", "event_state": False}
        levelling.insert_one(bot_data)

@client.command()
async def areload(ctx,addon):
    # Reloads the file, thus updating the Cog class.
    client.reload_extension(f"Addons.{addon}")
    await ctx.send("Success")
@client.command()
async def addons(ctx):
    # ✅ // ❌
    embed = discord.Embed(title="ADDON PACKAGES")

    # Clan System
    if os.path.exists("Addons/Clan System.py") is True:
        embed.add_field(name="Clan System", value="`Installed ✅`")
    else:
        embed.add_field(name="Clan System", value="`Installed ❌`")

    # Holiday System
    if os.path.exists("Addons/Holiday System.py") is True:
        embed.add_field(name="Holiday System", value="`Installed ✅`")
    else:
        embed.add_field(name="Holiday System", value="`Installed ❌`")

    # Vocal System
    if os.path.exists("Addons/Vocal System.py") is True:
        embed.add_field(name="Vocal System", value="`Installed ✅`")
    else:
        embed.add_field(name="Vocal System", value="`Installed ❌`")

    # Profile+
    if os.path.exists("Addons/Profile+.py") is True:
        embed.add_field(name="Profile+", value="`Installed ✅`")
    else:
        embed.add_field(name="Profile+", value="`Installed ❌`")

    # Extras+
    if os.path.exists("Addons/Extras+.py") is True:
        embed.add_field(name="Extras+", value="`Installed ✅`")
    else:
        embed.add_field(name="Extras+", value="`Installed ❌`")

    # Stats
    if os.path.exists("Addons/Stats.py") is True:
        embed.add_field(name="Stats", value="`Installed ✅`")
    else:
        embed.add_field(name="Stats", value="`Installed ❌`")

    # Events
    if os.path.exists("Addons/Events.py") is True:
        embed.add_field(name="Events", value="`Installed ✅`")
    else:
        embed.add_field(name="Events", value="`Installed ❌`")

    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    await client.process_commands(message) 
    if message.author.bot:
        return
    em = discord.Embed(title="Media Logger", decription=f'[Jump to Message]({message.jump_url})', color=0x32a852)
    em.add_field(name="** **", value=f'[Jump to Message]({message.jump_url})')
    em.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    em.set_footer(text=f'User ID: {message.author.id}| MSG ID: {message.id}')
    for message in message.attachments:
        if message.filename.endswith('.png') or message.filename.endswith('.jpeg') or message.filename.endswith('.gif') or message.filename.endswith('.jpg') or message.filename.endswith('.mp4') or message.filename.endswith('.mov'):
            file = await message.to_file()
            channel = client.get_channel(958868411021156363)
            if channel:
                await channel.send(file=file, embed=em)

logging.info("------------- Loading -------------")
for fn in listdir("Commands"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn}")
        client.load_extension(f"Commands.{fn[:-3]}")
        logging.info(f"Loaded {fn}")

for fn in listdir("Addons"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn} Addon")
        client.load_extension(f"Addons.{fn[:-3]}")
        logging.info(f"Loaded {fn} Addon")

logging.info(f"Loading Level System")
client.load_extension("Systems.levelsys")
logging.info(f"Loaded Level System")

logging.info("------------- Finished Loading -------------")


client.run("OTU2NjExODkxMjU2NTE2NjQ5.YjywPw.WhS74u_DiiDZBiHReb4-uer4U7Q")

# End Of Main
