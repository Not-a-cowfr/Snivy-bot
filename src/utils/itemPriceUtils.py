import discord
from discord.ext import tasks
import json
import time
import requests

def get_bz_item_data(item_name: str):
    url = "https://api.hypixel.net/skyblock/bazaar"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", {})
        item_data = products.get(item_name)
        if item_data:
            return item_data
        else:
            return f"Item '{item_name}' not found."
    else:
        return f"HTTP Error: {response.status_code}"
