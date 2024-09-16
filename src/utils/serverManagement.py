import discord
from discord.ext import tasks

from jsonDataUtils import getData
from guildUtils import get_hypixel_guild_data_by_guild

async def edit_role(role: discord.Role, name: str, color: int):
    try:
        await role.edit(name=name, color=color)
        print(f"Role '{name}' edited successfully with color #{color:06x}.")
        return role
    except discord.DiscordException as e:
        print(f"Failed to edit role '{name}': {e}")
        return None


async def create_role(guild: discord.Guild, name: str, color: int):
    try:
        # checks if the role already exists, if it does, then it edits the role instead
        role_exists = discord.utils.get(guild.roles, name=name)
        if role_exists:
            return await edit_role(role_exists, name, color)

        role = await guild.create_role(name=name, color=discord.Color(color))
        print(f"Role '{name}' created successfully with color #{color:06x}.")
        return role
    except discord.DiscordException as e:
        print(f"Failed to create role '{name}': {e}")
        return None

# loop hasnt yet been started in startBot.py
class isInGuild:
    def __init__(self, api_key):
        self.api_key = api_key

    @tasks.loop(minutes=15)
    async def isInGuild(self, guild: discord.Guild):
        # Get the guild data for "Snivy"
        guild_data = get_hypixel_guild_data_by_guild(self.api_key, "Snivy")
        if not isinstance(guild_data, dict):
            print(guild_data)
            return

        # Get the list of player UUIDs in the guild
        player_uuids = {member['uuid'] for member in guild_data.get('members', [])}

        # Check each member in the Discord guild
        for member in guild.members:
            user_id = str(member.id)
            minecraft_uuid = getData('src/data/userData.json', user_id, 'minecraft_uuid')

            if minecraft_uuid:
                if minecraft_uuid in player_uuids:
                    print(f"{member.name} is in Snivy")
                else:
                    print(f"{member.name} isn't in Snivy")
            else:
                print(f"{member.name} doesn't have a linked account")

