# Imports
from os import listdir

from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole, \
    NoPrivateMessage
import discord
from ruamel.yaml import YAML
import logging
import os
import requests
from dotenv import load_dotenv
from discord import Webhook, RequestsWebhookAdapter
from Systems.levelsys import levelling
from instagramy import InstagramUser
import asyncio
load_dotenv()

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless having issues with ruamel)
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Command Prefix + Removes the default discord.py help command
client = commands.Bot(command_prefix=commands.when_mentioned_or(config['Prefix']), intents=discord.Intents.all(), case_insensitive=True)
client.remove_command('help')

# sends discord logging files which could potentially be useful for catching errors.
os.remove("Logs/logs.txt")
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'
logging.basicConfig(filename='Logs/logs.txt', level=logging.DEBUG, format=FORMAT)
logging.debug('Started Logging')
logging.info('Connecting to Discord.')

os.environ['IG_USERNAME'] = 'eva.cudmore'
os.environ['TIME_INTERVAL'] = '5'
os.environ['WEBHOOK_URL'] = 'https://discord.com/api/webhooks/958993287606304788/iO59oLqIzSMtqnqm49RbGM1grOR3gr6VW7KjRtGKzhsCKKFss774ChDDG-ovgS8b04Xv'

IG_USERNAME = os.getenv('IG_USERNAME')
INSTAGRAM_USERNAME = os.environ.get('IG_USERNAME')
TIME_INTERVAL = os.environ.get('TIME_INTERVAL')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

web = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter())

def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


async def webhook(webhook_url, html):
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "@"+INSTAGRAM_USERNAME+"Has posted on Instagram!"
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    embed["image"] = {"url":get_last_thumb_url(html)} 
    data["embeds"].append(embed)
    guild = await client.fetch_guild(958418306753257473)
    role = discord.utils.get(guild.roles, name='Instagram')
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    web.send(role.mention)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html

#os.environ['LAST_IMAGE_ID'] = get_last_publication_url(get_instagram_html(INSTAGRAM_USERNAME))

async def main():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if(os.environ.get("LAST_IMAGE_ID") == get_last_publication_url(html)):
            pass
        else:
            os.environ["LAST_IMAGE_ID"] = get_last_publication_url(html)
            await webhook(os.environ.get("WEBHOOK_URL"),
                    get_instagram_html(INSTAGRAM_USERNAME))
    except Exception as e:
        print(e)

async def function():
    if __name__ == "__main__":
        if os.environ.get('IG_USERNAME') != None and os.environ.get('WEBHOOK_URL') != None:
            while True:
                await main()
                await asyncio.sleep(float(os.environ.get('TIME_INTERVAL') or 600))
        else:
            print('Please configure environment variables properly!')

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
    client.loop.create_task(function())
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

# Uses the bot token to login, so don't remove this.
token = os.getenv("DISCORD_TOKEN")
client.run(token)

# End Of Main
