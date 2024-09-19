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


def get_ah_item_data(item_names: list):
    url = "https://api.hypixel.net/skyblock/auctions"
    lowest_bins = {}

    for item_name in item_names:
        page = 0
        matching_auctions = []

        while True:
            response = requests.get(f"{url}?page={page}")
            print(page)
            if response.status_code == 200:
                data = response.json()
                auctions = data.get("auctions", [])
                for auction in auctions:
                    if auction.get("item_name", "").lower() == item_name.lower() and auction.get("bin") == True:
                        matching_auctions.append(auction)
                if page >= data.get("totalPages", 0) - 1:
                    break
                page += 1
            elif response.status_code == 404:
                print("HTTP Error 404: Resource not found")
                break
            else:
                print(f"HTTP Error: {response.status_code}")
                break

        if matching_auctions:
            starting_bids = [auction.get("starting_bid", float('inf')) for auction in matching_auctions]
            lowest_starting_bid = min(starting_bids)
            lowest_bins[item_name] = lowest_starting_bid
        else:
            lowest_bins[item_name] = None

    return lowest_bins


