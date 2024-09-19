from discord.ext import tasks
import time

from src.commands.bits import update_bz_bits_item_prices, update_ah_bits_item_prices
from src.utils.jsonDataUtils import saveLibraryData

@tasks.loop(minutes=30)
async def update_item_prices():
    update_bz_bits_item_prices()
    update_ah_bits_item_prices()
    saveLibraryData('src/data/serverData.json', 'bot_data', 'last_updated_bits_prices', time.time())
