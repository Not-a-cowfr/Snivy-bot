import discord
from discord.ext import tasks
import json
import time
import requests

#from src.botSetup import api_key

# loop hasnt yet been started in startBot.py
class check_bz_bits_items():
    def __init__(self):
        super().__init__()
        self.check_player_status.start()

    minutes = 20 # set how often it will start the check for the bazaar data
    @tasks.loop(minutes=minutes)
    async def get_bz_bits_items(self):
        with open('src/data/bits/itemData.json', 'r') as file:
            item_data = json.load(file)

        bz_items = item_data.get('bz_item_list', {})
        num_items = len(bz_items)

        global minutes
        sleep_duration = (minutes * 45) / num_items # gets all the data of the course of 3/4 the wait time

        def fetch_bazaar_data(item_name):
            url = f'https://api.hypixel.net/skyblock/bazaar'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('products', {}).get(item_name, {})
            else:
                print(f"Failed to fetch data for {item_name}: {response.status_code}")
                return {}

        for item_name in bz_items:
            item_data = fetch_bazaar_data(item_name)
            print(f"Data for {item_name}: {item_data}")
            time.sleep(sleep_duration)