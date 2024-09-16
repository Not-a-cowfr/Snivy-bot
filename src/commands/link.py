import requests
import json

def get_linked_discord(minecraft_username, hypixel_api_key, discord_user_id):
    mojang_url = f'https://api.mojang.com/users/profiles/minecraft/{minecraft_username}'
    mojang_response = requests.get(mojang_url)

    if mojang_response.status_code != 200:
        return False, f"Minecraft username {minecraft_username} does not exist"

    uuid = mojang_response.json().get('id')
    hypixel_url = f'https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}'
    hypixel_response = requests.get(hypixel_url)

    if hypixel_response.status_code != 200:
        return False, f"Failed to fetch data for Minecraft username {minecraft_username}"

    player_data = hypixel_response.json().get('player')
    if not player_data:
        return False, f"No data found for Minecraft username {minecraft_username}"

    linked_discord = player_data.get('socialMedia', {}).get('links', {}).get('DISCORD')
    if not linked_discord:
        return False, f"{minecraft_username} does not have a linked Discord account"

    if linked_discord != discord_user_id:
        return False, f"You do not have access to link to {minecraft_username}"

    return True, linked_discord