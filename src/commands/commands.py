from dataclasses import fields

from discord import app_commands, Interaction
import discord

from botSetup import bot, api_key
from commands.uptime import get_mojang_uuid, uptime as get_uptime
from commands.link import linkMinecraftAccount
from commands.guild import leaderboard as guild_leaderboard

from src.utils.embedUtils import color_embed
from src.utils.serverManagement import create_role, isSnivy
from src.utils.jsonDataUtils import loadData, saveLibraryData, getData
from src.utils.embedUtils import color_embed, success_embed, error_embed

data_file = 'src/data/userData.json'


def standalone_commands():
    #TODO add buttons to the report message for warn and mute (no kick or ban because misclicks are possible)
    @bot.tree.context_menu(name="Report Message")
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        
        report_channel = getData('src/data/serverData.json', interaction.guild_id, 'report_channel')
        if report_channel:
            fields = [
                ('Reported By', interaction.user.mention, True),
                ('Message', f'[Jump to message]({message.jump_url})', True)
            ]

            await error_embed(interaction,
                               title='Message Reported',
                               message=f'{message.content}\n-# sent by {message.author.mention}',
                               fields=fields,
                               channel=report_channel
                               )
            await interaction.response.send_message('Thank you for your report', ephemeral=True)
        else:
            await error_embed(interaction, title='Report Channel Not Set', message='The report channel has not yet been set')

    #TODO add buttons to the report message for warn and mute (no kick or ban because misclicks are possible)
    @bot.tree.context_menu(name="Report User")
    async def report_user(interaction: Interaction, user: discord.User):
        
        report_channel = getData('src/data/serverData.json', interaction.guild_id, 'report_channel')
        if report_channel:
            fields = [
                ('Reported By', interaction.user.mention, True),
                ('Reported User', user.mention, True)
            ]

            await error_embed(interaction,
                                title='User Reported',
                                fields=fields,
                                channel=report_channel
                                )
            await interaction.response.send_message('Thank you for your report', ephemeral=True)
        else:
            await error_embed(interaction, title='Report channel not set', message='The report channel has not yet been set')

    @bot.tree.context_menu(name='User Info')
    async def user_info(interaction: Interaction, user: discord.Member):
        

        fields = [
            ('ID', user.id, True),
            ('Name', user.name, True),
            ('Discriminator', user.discriminator, True),
            ('Joined At', user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), True)
        ]

        await color_embed(interaction, message='User Info - {user.name}', fields=fields, thumbnail=user.avatar.url, ephemeral=True)


    @bot.tree.context_menu(name='Get Linked Account')
    async def get_linked_account(interaction: Interaction, user: discord.Member):
        linked_users = loadData('src/data/userData.json')
        linked_account = linked_users.get(str(user.id), None)

        if linked_account:
            username = linked_account.get('username', 'No username linked')
            await interaction.response.send_message(f"{user.name}'s linked Minecraft account: `{username}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.name} has not linked their Minecraft account.", ephemeral=True)

    #TODO change /link from storing guild, to storing guild id
    @bot.tree.command(name='link', description='Link your Discord ID with your Minecraft username')
    @app_commands.describe(username='Your Minecraft username')
    async def link(interaction: discord.Interaction, username: str):
        
        user_id = str(interaction.user.id)
        discord_username = str(interaction.user)

        success, uuid, guild_name, error_message = linkMinecraftAccount(
            minecraft_username=username,
            hypixel_api_key=api_key,
            discord_user_id=user_id,
            discord_username=discord_username
        )

        if success:
            saveLibraryData('src/data/userData.json', user_id, 'username', username)
            saveLibraryData('src/data/userData.json', user_id, 'minecraft_uuid', uuid)
            saveLibraryData('src/data/userData.json', user_id, 'discord_username', discord_username)
            if guild_name:
                saveLibraryData('src/data/userData.json', user_id, 'guild', guild_name)
                await success_embed(interaction,
                              title='Linked Successfully!',
                              message=f'Linked your Discord account to **{username}** in the guild **{guild_name}**',
                              )
            else:
                await success_embed(interaction,
                                    title='Linked Successfully!',
                                    message=f'Linked your Discord account to **{username}**, but guild link was unsuccessful',
                                    )
        else:
            await error_embed(interaction, title='Link Unsuccessful', message=error_message, )

    @bot.tree.command(name='unlink', description='Unlink your Minecraft username and guild')
    async def unlink(interaction: discord.Interaction):
        
        user_id = str(interaction.user.id)
        linked_users = loadData(data_file)

        if linked_users.get(user_id, {}).get('username', '') == '':
            await error_embed(interaction, title='Unlink Unsuccessful', message='Your account is not linked to any username')
            return

        saveLibraryData(data_file, user_id, 'username', "")
        saveLibraryData(data_file, user_id, 'guild', "")

        await success_embed(interaction, title='Unlinked Successfully!', message='Unlinked your Minecraft username and guild from your Discord account.')

    @bot.tree.command(name='uptime', description='Get the uptime of a Minecraft player')
    @app_commands.describe(username='Your Minecraft username')
    async def uptime(interaction: Interaction, username: str = None):
        if username is None:
            username = getData(data_file, str(interaction.user.id), 'username')
            if username is None:
                await error_embed(interaction, title='No Linked Account', message='You have not linked your Minecraft account yet.')
                return

        await get_uptime(interaction, username)

    @bot.tree.command(name='color', description='Set your preferred color')
    @app_commands.describe(color='The color you want to set (in hexadecimal format, e.g., #3498db)')
    async def set_color(interaction: Interaction, color: str):
        user_id = str(interaction.user.id)
        linked_users = loadData(data_file)

        try:
            preferred_color = color.replace('#', '')[:6]  # removes all # characters from the hex
            int(preferred_color, 16)  # convert from hex to integer
        except ValueError:
            await interaction.response.send_message(
                'Invalid color format. Please use hexadecimal format (e.g., #3498db)', ephemeral=True)
            return

        if user_id not in linked_users:
            linked_users[user_id] = {}
        elif isinstance(linked_users[user_id], str):
            linked_users[user_id] = {'username': linked_users[user_id]}

        saveLibraryData(data_file, user_id, 'preferred_color', preferred_color)

        color = getData('src/data/userData.json', user_id, 'preferred_color')
        color = int(color, 16)

        role = await create_role(interaction.guild, name=interaction.user.display_name, color=color)
        if role is None:
            await color_embed(interaction, f'Your user color has been set to #{preferred_color}')

        await interaction.user.add_roles(role)

        embed = discord.Embed(title='', description=f'Your user color has been set to #{preferred_color}', color=color)
        await interaction.response.send_message(embed=embed)


class Admin(app_commands.Group):
    """@app_commands.command(name='delete_role')
    async def delete_role(interaction: Interaction, role: str):
        isAdmin(interaction)
        await role.delete()
        await success_embed(interaction, message=f'Deleted role {role.name}')"""


class Setup(app_commands.Group):
    """@app_commands.command(name='report_channel', description='Set the channel for reports to go to')
    async def set_report_channel(self, interaction: Interaction):
        saveLibraryData('src/data/serverData.json', interaction.guild_id, 'report_channel', interaction.channel_id)

        await success_embed(interaction, message=f'Set the report channel to <#{interaction.channel_id}>')

    @app_commands.command(name='admin_role', description='Set the admin role for the server')
    @app_commands.describe(role='Ping the role you want to set as admin')
    async def set_admin_role(self, interaction: Interaction, role: str):
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message('You do not have permission to use this command. Only the server owner can use this command.', ephemeral=True)
            return

        #TODO change the perms for running `/setup` and `/admin` to only the admin role

        saveLibraryData('src/data/serverData.json', interaction.guild_id, 'admin_role', role)

        await success_embed(interaction, message=f'Set the admin role to {role.mention}')"""


class Guild(app_commands.Group):
    """@app_commands.command(name='leaderboard', description='Top 10 players in guild xp this week')
    @app_commands.describe(guild_name='The name of the guild (optional)')
    async def leaderboard(self, interaction: discord.Interaction, guild_name: str = None):

        await guild_leaderboard(interaction, guild_name=guild_name)"""