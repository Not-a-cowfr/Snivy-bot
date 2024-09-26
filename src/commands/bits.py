import requests
from discord.ext import tasks
import json
import discord
from discord.ui import Button, View
import math

from src.utils.jsonDataUtils import loadData, saveLibraryData, getData
from src.utils.itemPriceUtils import get_bz_item_data, get_ah_item_data


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


def update_craft_bits_item_prices():
    # Initialize bz data
    bz_crafts = loadData('src/data/bits/crafts/bzCraftItems.json')
    bz_materials = loadData('src/data/bits/crafts/bzMaterials.json')
    ah_crafts = loadData('src/data/bits/crafts/ahCraftItems.json')
    ah_materials = loadData('src/data/bits/crafts/ahMaterials.json')

    # Update bz crafts
    for item in bz_crafts:
        if item:
            item_data = get_bz_item_data(item['item_id'])

            sell_summary = item_data.get('sell_summary', [])
            buy_summary = item_data.get('buy_summary', [])

            sell_prices = [entry['pricePerUnit'] for entry in sell_summary if 'pricePerUnit' in entry]
            buy_prices = [entry['pricePerUnit'] for entry in buy_summary if 'pricePerUnit' in entry]

            lowest_sell_price = min(sell_prices) if sell_prices else None
            highest_buy_price = min(buy_prices) if buy_prices else None

            saveLibraryData('src/data/bits/bzCraftItems.json', item['item_id'], 'instasell', lowest_sell_price)
            saveLibraryData('src/data/bits/bzCraftItems.json', item['item_id'], 'selloffer', highest_buy_price)

    # Same thing but for bz materials
    for item in bz_materials:
        if item:
            item_data = get_bz_item_data(item['item_id'])

            sell_summary = item_data.get('sell_summary', [])
            buy_summary = item_data.get('buy_summary', [])

            sell_prices = [entry['pricePerUnit'] for entry in sell_summary if 'pricePerUnit' in entry]
            buy_prices = [entry['pricePerUnit'] for entry in buy_summary if 'pricePerUnit' in entry]

            lowest_sell_price = min(sell_prices) if sell_prices else None
            highest_buy_price = min(buy_prices) if buy_prices else None

            saveLibraryData('src/data/bits/bzMaterials.json', item['item_id'], 'instasell', lowest_sell_price)
            saveLibraryData('src/data/bits/bzMaterials.json', item['item_id'], 'selloffer', highest_buy_price)

    # Create a dictionary for ah crafts and materials
    ah_items = {item['item_id']: None for item in ah_crafts if item}
    ah_items.update({item['item_id']: None for item in ah_materials if item})

    # Fetch AH data once
    items_data = get_ah_item_data(ah_items)

    # Update ah crafts
    for item in ah_crafts:
        ah_crafts_list = {}
        if item:
            ah_item_crafts[item] = None

    get_ah_item_data(ah_crafts_list)

    # Update ah materials
    for item in ah_materials:
        ah_materials_list = {}
        if item:
            ah_item_materials[item] = None

    get_ah_item_data(ah_materials_list)

#TODO add choosing between instabuy/instasell and sell offer/buy order
class BitsView(View):
    def __init__(self, results, interaction):
        super().__init__(timeout=120) # will time out after 2 minutes
        self.results = results
        self.interaction = interaction
        self.user_id = interaction.user.id
        self.current_page = 0
        self.items_per_page = 20
        self.use_selloffer = True
        self.update_buttons()

    def get_page_content(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_results = self.results[start:end]
        message = '\n'.join(
            [f'{index + 1}. **{name}**  |  `{format(round(ratio), ",")}` coins/bit **(**`{format(bits, ",")} bits`**)**'
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
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

    async def check_user(self, interaction: discord.Interaction): # only let thje preson who used the command press buttons
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You are not allowed to use these buttons.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_user(interaction):
            return
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_user(interaction):
            return
        if (self.current_page + 1) * self.items_per_page < len(self.results):
            self.current_page += 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Using Sell Offer", style=discord.ButtonStyle.secondary)
    async def switch_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_user(interaction):
            return
        self.use_selloffer = not self.use_selloffer
        button.label = "Use Insta Sell" if self.use_selloffer else "Use Sell Offer"
        await self.update_results()
        await self.update_embed(interaction)

    def update_buttons(self):
        self.previous_page.disabled = self.current_page == 0
        self.next_page.disabled = (self.current_page + 1) * self.items_per_page >= len(self.results)

    async def on_timeout(self):
        await self.interaction.edit_original_response(view=None)  # Remove the buttons

    async def update_results(self):
        bz_items = loadData('src/data/bits/bzItems.json')
        ah_items = loadData('src/data/bits/ahItems.json')
        self.results = []

        for item_id, item_info in bz_items.items():
            price = item_info.get('selloffer') if self.use_selloffer else item_info.get('instasell')
            bits = item_info.get('bits')
            name = item_info.get('name', 'item name not found!')
            emoji = item_info.get('emoji', '❓')
            if price and bits:
                ratio = price / bits
                self.results.append((f'{emoji} {name}', ratio, bits, price))

        for item_name, item_info in ah_items.items():
            lowest_bin = item_info.get('lowest_bin')
            bits = item_info.get('bits')
            name = item_info.get('name', item_name)
            emoji = item_info.get('emoji', '❓')
            if lowest_bin and bits:
                ratio = lowest_bin / bits
                self.results.append((f'{emoji} {name}', ratio, bits, lowest_bin))

        self.results.sort(key=lambda x: x[1], reverse=True)