import discord
from discord.ext import tasks
import json
import time
import requests

def get_bz_item_data(item_name: str):
    response = requests.get("https://api.hypixel.net/skyblock/bazaar")
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


def get_ah_item_data(item_names: list):
    url = "https://api.hypixel.net/skyblock/auctions"
    lowest_bins = {item_name: float('inf') for item_name in item_names}
    item_names_lower = [item_name.lower() for item_name in item_names]

    page = 0
    while True:
        response = requests.get(f"{url}?page={page}")
        if response.status_code == 200:
            data = response.json()
            auctions = data.get("auctions", [])
            for auction in auctions:
                item_name = auction.get("item_name", "").lower()
                item_name = item_name.replace('\u00e2\u201e\u00a2', '™').replace('\u00c2\u00a9', '©').replace('\u00c2\u00ae', '®')
                if item_name in item_names_lower and auction.get("bin") == True:
                    index = item_names_lower.index(item_name)
                    starting_bid = auction.get("starting_bid", float('inf'))
                    if starting_bid < lowest_bins[item_names[index]]:
                        lowest_bins[item_names[index]] = starting_bid
            if page >= data.get("totalPages", 0) - 1:
                break
            page += 1
        elif response.status_code == 404:
            print("HTTP Error 404: Resource not found")
            break
        else:
            print(f"HTTP Error: {response.status_code}")
            break

    for item_name in item_names:
        if lowest_bins[item_name] == float('inf'):
            lowest_bins[item_name] = None

    return lowest_bins


