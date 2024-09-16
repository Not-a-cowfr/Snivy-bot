from discord import app_commands, Interaction
import discord
import os

from botSetup import bot, api_key
from commands.report import ReportReasonModal
from commands.uptime import get_mojang_uuid, uptime as get_uptime
from commands.link import get_linked_discord

from src.utils.jsonDataUtils import loadData, saveUserData, getData

data_file = 'src/data/userData.json'

def standalone_commands():
    report_channel = bot.get_channel(1284630321073094808)
    mod_team_role_id = 1277802306464776295

    @bot.tree.context_menu(name="Report Message")
    async def report_message(interaction: Interaction, message: discord.Message):
        if report_channel:
            report_message = await report_channel.send(
                f"<@&{mod_team_role_id}>\n{interaction.user.mention} reported a message: {message.jump_url}"
            )

            modal = ReportReasonModal(report_message)
            await interaction.response.send_modal(modal)

    @bot.tree.context_menu(name="Report User")
    async def report_user(interaction: Interaction, user: discord.User):
        if report_channel:
            report_message = await report_channel.send(
                f"<@&{mod_team_role_id}>\n{interaction.user.mention} reported {user.mention}."
            )

            modal = ReportReasonModal(report_message)
            await interaction.response.send_modal(modal)

    @bot.tree.context_menu(name='User Info')
    async def user_info(interaction: Interaction, user: discord.Member):
        embed = discord.Embed(title=f'User Info - {user.name}', color=discord.Color.blue())
        embed.add_field(name='ID', value=user.id, inline=True)
        embed.add_field(name='Name', value=user.name, inline=True)
        embed.add_field(name='Discriminator', value=user.discriminator, inline=True)
        embed.add_field(name='Joined At', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.context_menu(name='Get Linked Account')
    async def get_linked_account(interaction: Interaction, user: discord.Member):
        global data_file
        linked_users = loadData(data_file)
        linked_account = linked_users.get(str(user.id), None)

        if linked_account:
            username = linked_account.get('username', 'No username linked')
            await interaction.response.send_message(f"{user.name}'s linked Minecraft account: `{username}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.name} has not linked their Minecraft account.", ephemeral=True)

    @bot.tree.command(name='link', description='Link your Discord ID with your Minecraft username')
    @app_commands.describe(username='Your Minecraft username')
    async def link(interaction: discord.Interaction, username: str):
        user_id = str(interaction.user.id)
        hypixel_api_key = api_key

        success, message = get_linked_discord(username, hypixel_api_key, str(interaction.user))
        if success:
            saveUserData(file_path='src/data/userData.json', user_id=user_id, data_type='username', data=username)
            await interaction.response.send_message(f"Linked your Discord account to {username}.")
        else:
            await interaction.response.send_message(f"{message}")

    @bot.tree.command(name='unlink', description='Unlink your Minecraft username')
    async def unlink(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        saveUserData('src/data/userData.json', user_id, 'username', "")
        await interaction.response.send_message("Unlinked your Minecraft username from your Discord account.")

    @bot.tree.command(name='uptime', description='Get the uptime of a Minecraft player')
    @app_commands.describe(username='Your Minecraft username')
    async def uptime(interaction: Interaction, username: str = None):
        user_id = str(interaction.user.id)
        linked_users = loadData(data_file)

        if user_id not in linked_users:
            linked_users[user_id] = {}

        if isinstance(linked_users[user_id], str):
            linked_users[user_id] = {'username': linked_users[user_id]}

        if username is None:
            username = linked_users[user_id].get('username')

            if username is None:
                await interaction.response.send_message('You have not linked your Minecraft account yet.')
                return

        await get_uptime(interaction, username)


    @bot.tree.command(name='color', description='Set your preferred embed color')
    @app_commands.describe(color='The color you want to set (in hexadecimal format, e.g., #3498db)')
    async def set_color(interaction: Interaction, color: str):
        user_id = str(interaction.user.id)
        linked_users = loadData(data_file)

        # Validate the color input
        if not color.startswith('#') or len(color) != 7:
            await interaction.response.send_message(
                'Invalid color format. Please use hexadecimal format (e.g., #3498db).', ephemeral=True)
            return

        try:
            preferred_color = color[1:]  # Remove the #
            int(preferred_color, 16)  # convert from hex to whatever the thing is that works
        except ValueError:
            await interaction.response.send_message(
                'Invalid color format. Please use hexadecimal format (e.g., #3498db).')
            return

        if user_id not in linked_users:
            linked_users[user_id] = {}
        elif isinstance(linked_users[user_id], str):
            linked_users[user_id] = {'username': linked_users[user_id]}

        saveUserData(data_file, user_id, 'preferred_color', preferred_color)

        color = getData('src/data/userData.json', user_id, 'preferred_color')
        if color is None:
            color = '0x3498db'
        else:
            color = int(f'0x{color}', 16)

        embed = discord.Embed(title=f'', description=f'Your preferred embed color has been set to #{preferred_color}', color=color)
        await interaction.response.send_message(embed=embed)
