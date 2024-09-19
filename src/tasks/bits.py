from discord.ext import tasks

from src.commands.bits import update_bz_bits_item_prices, update_ah_bits_item_prices

@tasks.loop(minutes=15)
async def update_item_prices():
    update_bz_bits_item_prices()
    update_ah_bits_item_prices()
