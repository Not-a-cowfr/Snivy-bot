from discord import app_commands

from src.utils.itemPriceUtils import get_ah_item_data
from src.utils.formatUtils import rarity_emoji

pet_types = [
    app_commands.Choice(name='Mining', value='mining'),
    app_commands.Choice(name='Combat', value='combat'),
    app_commands.Choice(name='Farming', value='farming'),
    app_commands.Choice(name='Foraging', value='foraging'),
    app_commands.Choice(name='Fishing', value='fishing'),
    app_commands.Choice(name='Alchemy', value='alchemy'),
]

mining = [
    'Armadillo',
    'Bat',
    'Endermite',
    'Goblin',
    'Mithril Golem',
    'Mole',
    'Rock',
    'Scatha',
    'Silverfish',
    'Wither Skeleton',
    'Snail',
]

combat = [
    'Ankylosaurus',
    'Black Cat',
    'Blaze',
    'Ender Dragon',
    'Enderman',
    'Ghoul',
    'Golden Dragon',  # remember to search for lvl 200 instead of level 100
    'Golem',
    'Grandma Wolf',
    'Griffin',
    'Horse',
    'Hound',
    'Jerry',
    'Kuudra',
    'Magma Cube',
    'Mammoth',
    'Phoenix',
    'Pigman',
    'Skeleton Horse',
    'Skeleton',
    'Snowman',
    'Spider',
    'Spirit',
    'Tarantula',
    'Tiger',
    'Turtle',
    'T-Rex',
    'Wolf',
    'Zombie',
    'Bal',
]

farming = ['Bee', 'Chickem', 'Elephant', 'Mooshroom Cow', 'Pig', 'Rabbit', 'Slug']

foraging = ['Ocealot', 'Giraffe', 'Lion', 'Monkey']

fishing = [
    'Ammonite',
    'Baby Yeti',
    'Blue Whale',
    'Dolphin',
    'Flying Fish',
    'Megladon',
    'Penguin',
    'Reindeer',
    'Spinosaurus',
    'Squid',
]

enchanting = ['Guardian']

alchemy = ['Jellyfish', 'Parrot', 'Sheep']


def get_pet_profit(type):
    pet_dict = {pet: None for pet in mining}
    ah_data = get_ah_item_data(pet_dict)

    result = []
    for pet, data in ah_data.items():
        price = data['lowest_bin']
        rarity = data['type']
        result.append(f'{rarity_emoji(rarity)}{pet} `{price}`')

    return '\n'.join(result)


# IDK how to do this, maybe profit divided by xp needed or smth to calculate the order? since its different for gdrag and also it gets the lbin, not the lbin lvl 1
