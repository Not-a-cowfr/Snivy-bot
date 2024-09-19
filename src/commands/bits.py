import requests
from discord.ext import tasks
import json
import discord
from discord.ui import Button, View

from src.utils.jsonDataUtils import loadData, saveLibraryData, getData
from src.utils.itemPriceUtils import get_bz_item_data, get_ah_item_data
from src.utils.embedUtils import color_embed


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
            highest_buy_price = min(buy_prices) if buy_prices else None

            # Save the updated prices
            saveLibraryData('src/data/bits/bzItems.json', item['item_id'], 'instasell', lowest_sell_price)
            saveLibraryData('src/data/bits/bzItems.json', item['item_id'], 'selloffer', highest_buy_price)


def update_ah_bits_item_prices():
    ah_items = loadData('src/data/bits/ahItems.json')

    item_list = list(ah_items.keys())

    items_data = get_ah_item_data(item_list)

    for item_name, lowest_bin in items_data.items():
        if lowest_bin is not None:
            saveLibraryData('src/data/bits/ahItems.json', item_name, 'lowest_bin', lowest_bin)


#DO NOT TOUCH THIS, YOU WILL BREAK IT
class BitsView(View):
    def __init__(self, results, interaction):
        super().__init__(timeout=60)
        self.results = results
        self.interaction = interaction
        self.current_page = 0
        self.items_per_page = 15

    def get_page_content(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_results = self.results[start:end]
        message = '\n'.join(
            [f'{index + 1}. {name}  |  `{format(round(ratio), ",")} coins per bit` **(**`{format(bits, ",")} bits`**)**'
             for index, (name, ratio, bits, price) in enumerate(page_results, start=start)])
        return message

    async def update_embed(self, interaction: discord.Interaction):
        content = self.get_page_content()

        user_id = str(interaction.user.id)
        color = getData('src/data/userData.json', user_id, 'preferred_color')
        if color is None:
            color = int('36393F', 16)
        else:
            color = int(color, 16)

        embed = discord.Embed(description=content, color=color)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (self.current_page + 1) * self.items_per_page < len(self.results):
            self.current_page += 1
            await self.update_embed(interaction)
