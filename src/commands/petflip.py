from discord import app_commands

pet_types = [
    app_commands.Choice(name='Mining', value="mining"),
    app_commands.Choice(name='Combat', value="combat"),
    app_commands.Choice(name='Farming', value="farming"),
    app_commands.Choice(name='Foraging', value="foraging"),
    app_commands.Choice(name='Fishing', value="fishing"),
    app_commands.Choice(name='Alchemy', value="alchemy")
]