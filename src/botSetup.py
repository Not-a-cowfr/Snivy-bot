import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.utils.fuckJson import UserDataAdapter
from src.utils.jsonDataUtils import loadData

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
api_key = os.getenv('API_KEY', '[ERROR] Api Key not found')

dtb = UserDataAdapter()

data = loadData("data/userData.json")

#   Put data from funny file into dtb
"""for key, value in data.items():
    id = key
    color = value.get("preferred_color")
    username = value.get("username")
    uuid = value.get("minecraft_uuid")
    dcuser = value.get("discord_username")
    guild = value.get("guild")

    dtb.insert_user(
        user_id=id,
        preferred_color=color,
        username=username,
        minecraft_uuid=uuid,
        discord_username=dcuser,
        guild=guild

    )"""


