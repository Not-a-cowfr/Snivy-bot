import requests
from discord.ext import tasks
import json

from src.utils.jsonDataUtils import loadData, saveLibraryData
from src.utils.itemPriceUtils import get_bz_item_data


def get_bz_bits_items_data():
    bz_items = loadData('src/data/bits/bzItems.json')

    items_data = []

    for item_id, item_info in bz_items.items():
        instasell = item_info.get('instasell')
        selloffer = item_info.get('selloffer')
        items_data.append({
            'item_id': item_id,
            'instasell': instasell,
            'selloffer': selloffer
        })

    return items_data, bz_items


def update_bz_bits_item_prices():
    items_data, bz_items = get_bz_bits_items_data()

    for item in items_data:
        if item:
            # Fetch the latest data for the item
            item_data = get_bz_item_data(item['item_id'])

            # Extract the sell and buy prices
            sell_summary = item_data.get('sell_summary', [])
            buy_summary = item_data.get('buy_summary', [])

            sell_prices = [entry['pricePerUnit'] for entry in sell_summary if 'pricePerUnit' in entry]
            buy_prices = [entry['pricePerUnit'] for entry in buy_summary if 'pricePerUnit' in entry]

            lowest_sell_price = min(sell_prices) if sell_prices else None
            highest_buy_price = max(buy_prices) if buy_prices else None

            # Save the updated prices
            saveLibraryData('src/data/bits/bzItems.json', item['item_id'], 'instasell', lowest_sell_price)
            saveLibraryData('src/data/bits/bzItems.json', item['item_id'], 'selloffer', highest_buy_price)

