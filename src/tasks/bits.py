import requests
from discord import tasks

from src.utils.jsonDataUtils import loadData, saveLibraryData

def get_bz_item_data(item_id: str):
    url = "https://api.hypixel.net/skyblock/bazaar"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", {})
        item_data = products.get(item_id)
        if item_data:
            return item_data
        else:
            return f"Item '{item_id}' not found."
    else:
        return f"HTTP Error: {response.status_code}"


def get_bz_bits_items_data():
    item_data = loadData('src/data/bits/itemData.json')
    bz_items = item_data.get("bz_item_list", {})
    items_data = []

    for item_name, item_info in bz_items.items():
        item_id = item_info.get("item_id")
        if item_id:
            item_data = get_bz_item_data(item_id)
            items_data.append(item_data)
        else:
            items_data.append(None)

    return items_data, bz_items


def update_bz_bits_item_prices():
    items_data, bz_items = get_bz_bits_items_data()

    for item in items_data:
        if item:
            sell_summary = item.get('sell_summary', [])
            buy_summary = item.get('buy_summary', [])

            sell_prices = [entry['pricePerUnit'] for entry in sell_summary if 'pricePerUnit' in entry]
            buy_prices = [entry['pricePerUnit'] for entry in buy_summary if 'pricePerUnit' in entry]

            lowest_sell_price = min(sell_prices) if sell_prices else None
            highest_buy_price = max(buy_prices) if buy_prices else None

            saveLibraryData('src/data/bits/bzItems.json', item['product_id'], 'instasell', lowest_sell_price)
            saveLibraryData('src/data/bits/bzItems.json', item['product_id'], 'sellorder', highest_buy_price)

class update_bits_items():
    @tasks.loop(minutes=10)
    async def bz_bits_items(self):
        update_bz_bits_item_prices()