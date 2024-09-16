import os
import json
import requests

def get_linked_discord(minecraft_username, hypixel_api_key, discord_user_id):
    mojang_url = f'https://api.mojang.com/users/profiles/minecraft/{minecraft_username}'
    mojang_response = requests.get(mojang_url)

    if mojang_response.status_code != 200:
        return False, f"Minecraft username **{minecraft_username}** does not exist", None

    uuid = mojang_response.json().get('id')
    hypixel_url = f'https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}'
    hypixel_response = requests.get(hypixel_url)

    player_data = hypixel_response.json().get('player')
    linked_discord = player_data.get('socialMedia', {}).get('links', {}).get('DISCORD')

    guild_url = f'https://api.hypixel.net/guild?key={hypixel_api_key}&player={uuid}'
    guild_response = requests.get(guild_url)

    if hypixel_response.status_code != 200:
        return False, f"Failed to fetch data for Minecraft username **{minecraft_username}** `{hypixel_response.status_code}`", None
    elif not player_data:
        return False, f"No data found for Minecraft username **{minecraft_username}**", None
    elif not linked_discord:
        return False, f"**{minecraft_username}** does not have a linked Discord account", None
    elif linked_discord != discord_user_id:
        return False, f"You do not have access to link to ****{minecraft_username}****", None
    elif guild_response.status_code != 200:
        return False, f"Failed to fetch guild data for Minecraft username **{minecraft_username}** `{guild_response.status_code}`", None

    guild_data = guild_response.json().get('guild')
    guild_name = guild_data.get('name') if guild_data else None

    return True, linked_discord, guild_name