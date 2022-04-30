import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

client_token = os.getenv("live_token")

#Application name	Discord Bot
#API key	0156719bb1a375b0e85541a5a3d27fd1
#Shared secret	3e2f9c19b1e4089e3259c8392699bd96
#Registered to	chasek04
lastfm_api_key = "0156719bb1a375b0e85541a5a3d27fd1"
lastfm_root_url = "http://ws.audioscrobbler.com/2.0/"
lastfm_shared_secret = "3e2f9c19b1e4089e3259c8392699bd96"

#http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=chasek04&api_key=3e2f9c19b1e4089e3259c8392699bd96&format=json
client_session = aiohttp.ClientSession()