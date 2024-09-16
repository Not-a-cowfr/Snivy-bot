import discord
import requests
from discord.ext import commands

from src.botSetup import api_key
from src.utils.jsonDataUtils import loadData

from src.utils.jsonDataUtils import getData

def get_mojang_uuid(player_name):
    if not player_name:
        return None, "You have not linked your Minecraft account yet."

    url = f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("id"), None
    else:
        return None, f"Error fetching UUID: {response.status_code}"


def get_username_from_uuid(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "name" in data:
            return data["name"]
        else:
            return "No username found for this UUID."
    elif response.status_code == 404:
        return "Username not found (UUID may be invalid)."
    else:
        return f"Error fetching username: {response.status_code}"


def get_hypixel_guild_data(api_key, player_uuid):
    url = "https://api.hypixel.net/guild"
    params = {
        "key": api_key,
        "player": player_uuid
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            guild = data.get("guild")
            exp_history = None
            for member in guild.get("members", []):
                if member.get("uuid") == player_uuid:
                    exp_history = member.get("expHistory")
                    break
            if exp_history:
                formatted_exp_history = {}
                for date, exp in exp_history.items():
                    hours = exp // 9000
                    minutes = (exp % 9000) / 150
                    formatted_exp_history[date] = f"{hours}:{round(minutes)}"
                return formatted_exp_history
            else:
                return "Player UUID not found in guild members."
        else:
            return f"Error: {data.get('cause')}"
    else:
        return f"HTTP Error: {response.status_code}"

def get_hypixel_guild_data_by_guild(api_key, guild_name):
    url = "https://api.hypixel.net/guild"
    params = {
        "key": api_key,
        "name": guild_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("guild")
        else:
            return f"Error: {data.get('cause')}"
    else:
        return f"HTTP Error: {response.status_code}"

async def leaderboard(interaction: discord.Interaction, guild_name: str = None):
    await interaction.response.defer()

    user_id = str(interaction.user.id)
    linked_users = loadData('src/data/userData.json')

    if user_id not in linked_users:
        linked_users[user_id] = {}
    elif isinstance(linked_users[user_id], str):
        linked_users[user_id] = {'username': linked_users[user_id]}

    if not guild_name:
        guild_name = linked_users[user_id].get('guild')
        if not guild_name:
            await interaction.followup.send('You have not linked your Hypixel guild')
            return

    color = getData('src/data/userData.json', user_id, 'preferred_color')
    if color is None:
        color = int('36393F', 16)
    else:
        color = int(color, 16)

    player_uuid, error_message = get_mojang_uuid(guild_name)
    if error_message:
        await interaction.followup.send(error_message)
        return

    if guild_name:
        guild_data = get_hypixel_guild_data_by_guild(api_key, guild_name)
        if isinstance(guild_data, dict):
            player_xp = []
            for member in guild_data.get('members', []):
                uuid = member.get('uuid')
                total_xp = sum(member.get('expHistory', {}).values())
                player_xp.append((uuid, total_xp))

            top_players = sorted(player_xp, key=lambda x: x[1], reverse=True)[:10]

            names = []
            xps = []
            for position, (player, xp) in enumerate(top_players, start=1):
                names.append(f"#{position} **{get_username_from_uuid(player)}**")
                xps.append(f"{xp:,} XP")

            embed = discord.Embed(title=f'Top 10 Players in **{guild_name}** for gexp this week', color=color)
            embed.add_field(name="", value="\n".join(names), inline=True)
            embed.add_field(name="", value="\n".join(xps), inline=True)

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(guild_data)
