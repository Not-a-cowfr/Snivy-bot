import discord
from discord.ext import tasks
import json
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

#TODO change the update ah bits function to work with the new ah system
def get_ah_item_data(item_rarities: dict):
    item_data = {item_name: {"lowest_bin": float('inf'), "type": None} for item_name in item_rarities}

    item_names_lower = {item_name.lower(): item_name for item_name in item_rarities}

    page = 0
    while True:
        response = requests.get(f"https://api.hypixel.net/skyblock/auctions?page={page}")
        print(page)

        if response.status_code == 200:
            data = response.json()
            auctions = data.get("auctions", [])

            for auction in auctions:
                # Get the item name and rarity from the auction data
                item_name = auction.get("item_name", "").lower()
                item_rarity = auction.get("tier", "Unknown").upper()

                # Replace special characters in item names
                item_name = item_name.replace('\u00e2\u201e\u00a2', '™').replace('\u00c2\u00a9', '©').replace(
                    '\u00c2\u00ae', '®')

                for search_name_lower, original_name in item_names_lower.items():
                    search_rarity = item_rarities[original_name] # gets the wanted rarity for the item
                    search_rarity = search_rarity.upper() if search_rarity is not None else None

                    # checks if the item in the auction api is
                    # 1. the same as the inputted item name
                    # 2. is a bin
                    # 3. rarity is the same as inputted rarity (if no rarity inputted it won't check for rarity)
                    if search_name_lower in item_name and auction.get("bin") is True and (search_rarity == "" or search_rarity is None or item_rarity == search_rarity):
                        starting_bid = auction.get("starting_bid", float('inf'))
                        # Update the lowest BIN price if the current starting bid is lower
                        if starting_bid < item_data[original_name]["lowest_bin"]:
                            item_data[original_name]["lowest_bin"] = starting_bid
                            item_data[original_name]["type"] = item_rarity

            # stops searching through pages if its on the last page
            if page >= data.get("totalPages", 0) - 1:
                break
            page += 1
        else:
            print(f"HTTP Error: {response.status_code}")
            break

    # set the return to an error message instead of inf if no price was found
    for item_name in item_rarities:
        if item_data[item_name]["lowest_bin"] == float('inf'):
            item_data[item_name]["lowest_bin"] = 'No price found!'

    return item_data


