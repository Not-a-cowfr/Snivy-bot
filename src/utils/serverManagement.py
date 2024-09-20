import discord
from discord.ext import tasks

from utils.jsonDataUtils import getData
from utils.guildUtils import get_hypixel_guild_data_by_guild

from src.botSetup import api_key
from src.utils.embedUtils import error_embed


async def edit_role(role: discord.Role, name: str, color: int):
    if color == 0:
        color = 1 # idk why but if its pure black it just uses the default color

    await role.edit(name=name, color=color)
    return role

async def create_role(guild: discord.Guild, name: str, color: int):
    # checks if the role already exists, if it does, then just edit the role
    role_exists = discord.utils.get(guild.roles, name=name)
    if role_exists:
        return await edit_role(role_exists, name, color)

    role = await guild.create_role(name=name, color=discord.Color(color))

    # makes the position of the new role 1 below the bot role
    bot_role = max(guild.me.roles, key=lambda r: r.position)
    await edit_role(role, name, color)
    await role.edit(position=bot_role.position - 1)
    print(f'creating role at position {bot_role.position - 1} (one below {bot_role})') # DO NOT REMOVE!!!! IT DOES NOT WORK CORRECTLY WITHOUT THIS, no, i dont know why

    return role

async def isSnivy(interaction: discord.Interaction):
    guild = interaction.guild
    if guild.id == 1277801084097658882:
        return True
    else:
        await error_embed(title='This doesnt look like my server...', message='This bot is only available in the **Snivy guild**\n\nhttps://discord.gg/Bu2KwE2U')


class isInGuild:
    def __init__(self, api_key):
        self.api_key = api_key
        self.guild = None

    def start(self, guild: discord.Guild):
        self.guild = guild
        self.isInGuild.start()

    @tasks.loop(minutes=1)
    async def isInGuild(self):
        if self.guild is None:
            return

        # gets the guild data for snivy
        guild_data = get_hypixel_guild_data_by_guild(self.api_key, "Snivy")
        if not isinstance(guild_data, dict):
            print(guild_data)
            return

        # gets the list of player UUIDs in the guild
        player_uuids = {member['uuid'] for member in guild_data.get('members', [])}

        # check each person in the discord if their linked account is in the guild
        for member in self.guild.members:
            user_id = str(member.id)
            minecraft_uuid = getData('src/data/userData.json', user_id, 'minecraft_uuid')

            if minecraft_uuid:
                if minecraft_uuid in player_uuids:
                    print(f"{member.name} is in Snivy")
                else:
                    print(f"{member.name} isn't in Snivy")
            else:
                print(f"{member.name} doesn't have a linked account")

