from discord import app_commands, Interaction
import discord
import os
from datetime import datetime, timezone

from botSetup import bot, api_key
from commands.report import ReportReasonModal
from commands.uptime import get_mojang_uuid, uptime as get_uptime
from commands.link import linkMinecraftAccount
from commands.guild import leaderboard as guild_leaderboard

from src.utils.serverManagement import create_role, isSnivy
from src.utils.jsonDataUtils import loadData, saveUserData, getData

data_file = 'src/data/userData.json'


def standalone_commands():
    report_channel = bot.get_channel(1284630321073094808)
    mod_team_role_id = 1277802306464776295

    @bot.tree.context_menu(name="Report Message")
    async def report_message(interaction: Interaction, message: discord.Message):
        #await isSnivy(interaction, discord.Guild)
        if report_channel:
            embed = discord.Embed(
                title="Message Report",
                color=discord.Color.red()
            )
            embed.add_field(name="", value=f'{message.content}\n\n', inline=False)
            embed.add_field(name="Reported By", value=interaction.user.mention, inline=True)
            embed.add_field(name="Message", value=f'[Jump to message]({message.jump_url})', inline=True)

            report_message = await report_channel.send(embed=embed)

            modal = ReportReasonModal(report_message)
            await interaction.response.send_modal(modal)

    @bot.tree.context_menu(name="Report User")
    async def report_user(interaction: Interaction, user: discord.User):
        #await isSnivy(interaction, discord.Guild)
        if report_channel:
            embed = discord.Embed(
                title="User Report",
                color=discord.Color.red()
            )
            embed.add_field(name="Reported User", value=user.mention, inline=True)
            embed.add_field(name="Reported By", value=interaction.user.mention, inline=True)

            report_message = await report_channel.send(embed=embed)

            modal = ReportReasonModal(report_message)
            await interaction.response.send_modal(modal)

    @bot.tree.context_menu(name='User Info')
    async def user_info(interaction: Interaction, user: discord.Member):
        #await isSnivy(interaction, discord.Guild)
        user_id = str(interaction.user.id)
        color = getData('src/data/userData.json', user_id, 'preferred_color')
        if color is None:
            color = int('36393F', 16)
        else:
            color = int(color, 16)

        embed = discord.Embed(title=f'User Info - {user.name}', color=color)
        embed.add_field(name='ID', value=user.id, inline=True)
        embed.add_field(name='Name', value=user.name, inline=True)
        embed.add_field(name='Discriminator', value=user.discriminator, inline=True)
        embed.add_field(name='Joined At', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.context_menu(name='Get Linked Account')
    async def get_linked_account(interaction: Interaction, user: discord.Member):
        #await isSnivy(interaction, discord.Guild)
        global data_file
        linked_users = loadData(data_file)
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
        #await isSnivy(interaction, discord.Guild)
        user_id = str(interaction.user.id)
        discord_username = str(interaction.user)
        hypixel_api_key = api_key

        success, uuid, guild_name, error_message = linkMinecraftAccount(
            minecraft_username=username,
            hypixel_api_key=hypixel_api_key,
            discord_user_id=user_id,
            discord_username=discord_username
        )

        if success:
            saveUserData(file_path='src/data/userData.json', user_id=user_id, data_type='username', data=username)
            saveUserData(file_path='src/data/userData.json', user_id=user_id, data_type='minecraft_uuid', data=uuid)
            saveUserData(file_path='src/data/userData.json', user_id=user_id, data_type='discord_username', data=discord_username)
            if guild_name:
                saveUserData(file_path='src/data/userData.json', user_id=user_id, data_type='guild', data=guild_name)
                title = "Linked Successfully!"
                description = f"Linked your Discord account to **{username}** in the guild **{guild_name}**"
            else:
                title = "Linked Successfully!"
                description = f"Linked your Discord account to **{username}**, but guild link was unsuccessful"
        else:
            title = "Link Unsuccessful"
            description = error_message

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green() if success else discord.Color.red()
        )

        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='unlink', description='Unlink your Minecraft username and guild')
    async def unlink(interaction: discord.Interaction):
        #await isSnivy(interaction, discord.Guild)
        user_id = str(interaction.user.id)
        saveUserData('src/data/userData.json', user_id, 'username', "")
        saveUserData('src/data/userData.json', user_id, 'guild', "")

        embed = discord.Embed(
            title="Unlinked Successfully!",
            description="Unlinked your Minecraft username and guild from your Discord account.",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='uptime', description='Get the uptime of a Minecraft player')
    @app_commands.describe(username='Your Minecraft username')
    async def uptime(interaction: Interaction, username: str = None):
        #await isSnivy(interaction, discord.Guild)
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

        saveUserData(data_file, user_id, 'preferred_color', preferred_color)

        color = getData('src/userData.json', user_id, 'preferred_color')
        color = int(color, 16)

        role = await create_role(interaction.guild, name=interaction.user.display_name, color=color)
        if role is None:
            embed = discord.Embed(title='',
                                  description='Failed to create or edit the role. Ensure the bot has the "Manage Roles" permission.',
                                  color=color)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.user.add_roles(role)

        embed = discord.Embed(title='', description=f'Your user color has been set to #{preferred_color}', color=color)
        await interaction.response.send_message(embed=embed)


def server_setup_commands():
    bot.tree.command(name='set_report_channel', description='Set the channel for reports to go to')
    async def set_report_channel(interaction: Interaction):
        #await isSnivy(interaction, discord.Guild)
        global report_channel_id
        report_channel_id = interaction.channel_id
        await interaction.response.send_message(f'Set the report channel to <#{report_channel_id}>')


class guild(app_commands.Group):
    @app_commands.command(name='leaderboard', description='Top 10 players in guild xp this week')
    @app_commands.describe(guild_name='The name of the guild (optional)')
    async def leaderboard(self, interaction: discord.Interaction, guild_name: str = None):
        #await isSnivy(interaction, discord.Guild)
        await guild_leaderboard(interaction, guild_name=guild_name)