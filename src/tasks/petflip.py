from discord import tasks

from src.utils.itemPriceUtils import get_ah_item_data
from src.commands.petflip import mining, combat, farming, foraging, fishing, enchanting, alchemy

@tasks.loop(minutes=30)
async def