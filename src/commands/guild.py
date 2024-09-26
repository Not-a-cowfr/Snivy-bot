from dataclasses import fields

import discord
import requests
from discord.ext import commands

from src.botSetup import api_key

from src.utils.jsonDataUtils import getData, loadData
from src.utils.playerUtils import get_hypixel_guild_data_by_guild, get_mojang_uuid, get_username_from_uuid
from src.utils.formatUtils import online_emoji
from src.utils.embedUtils import color_embed, error_embed

#TODO add view to change average scope between 1 day, 3 days, and 1 week (1 week by default)
#TODO change /link from storing guild, to storing guild id
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
            return 'You have not linked your Hypixel guild'

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
                names.append(f"#{position}   {online_emoji(player)} **{get_username_from_uuid(player)}**")
                xps.append(f"{xp:,} XP")

            #TODO change this to use color_embed()
            embed = discord.Embed(title=f'Top 10 Players in **{guild_name}** for gexp this week', color=color)
            embed.add_field(name="", value="\n".join(names), inline=True)
            embed.add_field(name="", value="\n".join(xps), inline=True)

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(guild_data)

async def guild_uptime(interaction: discord.Interaction, guild: str = None):
    await interaction.response.defer()

    user_id = str(interaction.user.id)
    linked_users = loadData('src/data/userData.json')

    if user_id not in linked_users:
        linked_users[user_id] = {}
    elif isinstance(linked_users[user_id], str):
        linked_users[user_id] = {'username': linked_users[user_id]}

    if not guild:
        guild = linked_users[user_id].get('guild')
        if not guild:
            await error_embed(interaction, title='No linked guild!',
                              message='You have not linked your Hypixel guild with `/link` yet.')
            return

    guild_data = get_hypixel_guild_data_by_guild(api_key, guild)

    if not guild_data or 'members' not in guild_data:
        await error_embed(interaction, title='Error', message='Could not retrieve guild data.')
        return

    exp_per_member = []
    total_guild_exp = 0

    # Iterate through each member in the guild
    for member in guild_data['members']:
        total_exp = sum(member['expHistory'].values())
        total_guild_exp += total_exp
        total_exp = total_exp / 7
        total_hours = int(total_exp // 9000)
        total_minutes = int((total_exp % 9000) / 150)
        exp_per_member.append((member['uuid'], total_exp, f'{total_hours}h {total_minutes:.0f}m'))

    # Sort members by total experience and get the top 10
    sorted_members = sorted(exp_per_member, key=lambda x: x[1], reverse=True)[:10]

    names = []
    uptimes = []

    for position, (uuid, xp, uptime) in enumerate(sorted_members, start=1):
        player = get_username_from_uuid(uuid)
        names.append(f"#{position}   {online_emoji(uuid)} **{player}**")
        uptimes.append(uptime)

    total_guild_hours = int(total_guild_exp // 9000)
    total_guild_minutes = int((total_guild_exp % 9000) / 150)

    fields = [
        ("Player", "\n".join(names), True),
        ("Uptime", "\n".join(uptimes), True),
        ('', f'Total Guild uptime this week: **{total_guild_hours:,}** hours **{total_guild_minutes}** minutes', False)
    ]

    await color_embed(interaction, title=f'Average Uptime Leaderboard for **{guild}**', fields=fields)
