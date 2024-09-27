import os
import json
import requests

from src.utils.jsonDataUtils import saveLibraryData


def linkMinecraftAccount(
    minecraft_username, hypixel_api_key, discord_user_id, discord_username
):
    mojang_url = (
        f'https://api.mojang.com/users/profiles/minecraft/{minecraft_username.lower()}'
    )
    mojang_response = requests.get(mojang_url)

    if mojang_response.status_code != 200:
        return (
            False,
            None,
            None,
            f'Minecraft username **{minecraft_username}** does not exist',
        )

    uuid = mojang_response.json().get('id')
    hypixel_url = f'https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}'
    hypixel_response = requests.get(hypixel_url)

    if hypixel_response.status_code != 200:
        return (
            False,
            None,
            None,
            f'Failed to fetch data for Minecraft username **{minecraft_username}** {hypixel_response.status_code}`',
        )

    player_data = hypixel_response.json().get('player')
    if not player_data:
        return (
            False,
            None,
            None,
            f'No data found for Minecraft username **{minecraft_username}**',
        )

    linked_discord = player_data.get('socialMedia', {}).get('links', {}).get('DISCORD')
    if not linked_discord:
        return (
            False,
            None,
            None,
            f'**{minecraft_username}** does not have a linked Discord account',
        )
    elif linked_discord.lower() != discord_username.lower():
        return (
            False,
            None,
            None,
            f'You do not have access to link to **{minecraft_username}**',
        )

    guild_url = f'https://api.hypixel.net/guild?key={hypixel_api_key}&player={uuid}'
    guild_response = requests.get(guild_url)

    if guild_response.status_code != 200:
        return (
            False,
            None,
            None,
            f'Failed to fetch guild data for Minecraft username **{minecraft_username}** `{guild_response.status_code}`',
        )

    guild_data = guild_response.json().get('guild')
    guild_name = guild_data.get('name') if guild_data else None

    # Store the user's Discord username
    user_data = {
        'minecraft_uuid': uuid,
        'guild': guild_name,
        'discord_username': discord_username,
    }

    return True, uuid, guild_name, None
