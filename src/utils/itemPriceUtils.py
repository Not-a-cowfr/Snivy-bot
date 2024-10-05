import discord
from discord.ext import tasks
import json
import requests
from requests.exceptions import ChunkedEncodingError
import time
from tqdm import tqdm

def get_bz_item_data(item_id, retries=3, delay=2):
    url = 'https://api.hypixel.net/skyblock/bazaar'
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            return data.get('products', {}).get(item_id, {})
        except ChunkedEncodingError:
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

# take list, return dict with None as values for each item
# useful for inputting a list of items to get_ah_item_data when you dont care about rarity
def item_list_to_dict(items):
    return {item: None for item in items}

def get_ah_item_data(item_rarities: dict):
    item_data = {
        item_name: {'lowest_bin': float('inf'), 'type': None}
        for item_name in item_rarities
    }

    item_names_lower = {item_name.lower(): item_name for item_name in item_rarities}

    # initialize variables 🥺
    page = 0
    total_pages = 1

    # get the total number of pages (for the progress bar, i SWEAR this is useful)
    response = requests.get('https://api.hypixel.net/skyblock/auctions?page=0')
    if response.status_code == 200:
        total_pages = response.json().get('totalPages', 1)

    # tqdm = super sick ass progress bar
    with tqdm(total=total_pages, desc="Fetching auction data", bar_format="{desc}: {percentage:3.0f}%|{bar}| page {n_fmt}/{total_fmt}, [{rate_fmt}]") as pbar:
        while page < total_pages:
            response = requests.get(
                f'https://api.hypixel.net/skyblock/auctions?page={page}'
            )

            # use your brain, if request goes through and data is returned
            if response.status_code == 200:
                data = response.json()
                auctions = data.get('auctions', [])

                # searches every auction in the returned page of auctions
                for auction in auctions:

                    # lower cases item name and upper cases rarity for case insensitivity
                    item_name = auction.get('item_name', '').lower()
                    item_rarity = auction.get('tier', 'Unknown').upper()

                    # idk why but these symbols get converted to UTF-8 or whatever so i convert it back, idk
                    item_name = (
                        item_name.replace('\u00e2\u201e\u00a2', '™')
                        .replace('\u00c2\u00a9', '©')
                        .replace('\u00c2\u00ae', '®')
                    )

                    # checks if the item name is in the list of items to search for
                    for search_name_lower, original_name in item_names_lower.items():
                        search_rarity = item_rarities[
                            original_name
                        ]
                        search_rarity = (
                            # convert rarity to uppercase if it exists, if it doesnt exist, sets it to none
                            search_rarity.upper() if search_rarity is not None else None
                        )

                        # checks if the search name is in the item name and the auction is a BIN auction
                        if (
                            search_name_lower in item_name
                            and auction.get('bin') is True
                            and (
                                search_rarity == ''
                                or search_rarity is None
                                or item_rarity == search_rarity
                            )
                        ):
                            starting_bid = auction.get('starting_bid', float('inf'))
                            if starting_bid < item_data[original_name]['lowest_bin']:
                                item_data[original_name]['lowest_bin'] = starting_bid
                                item_data[original_name]['type'] = item_rarity

                page += 1
                pbar.update(1) # update progress bar
            else:
                print(f'HTTP Error: {response.status_code}')
                break

    for item_name in item_rarities:
        if item_data[item_name]['lowest_bin'] == float('inf'):
            item_data[item_name]['lowest_bin'] = None  # return None instead of 'inf' as lowest bin if no BIN auctions found
            # NOTE: this will still override any current price if youre saving this data, amke sure to add a check to stop this if you dont want it happening

    return item_data