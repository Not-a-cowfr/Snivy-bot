from code import interact
from dataclasses import fields
from discord import app_commands, Interaction
from discord.ext import commands
import discord
from discord.errors import NotFound
from botSetup import bot, api_key
from commands.uptime import get_mojang_uuid, uptime as get_uptime
from commands.link import linkMinecraftAccount
from commands.guild import leaderboard as guild_leaderboard, guild_uptime
from commands.petflip import pet_types, get_pet_profit
from commands.bits import (
    update_bz_bits_item_prices,
    update_ah_bits_item_prices,
    BitsView,
)

from src.utils.fuckJson import UserDataAdapter
from src.utils.playerUtils import get_username_from_uuid
from src.utils.serverManagement import create_role, isSnivy
from src.utils.jsonDataUtils import loadData, saveLibraryData, getData
from src.utils.embedUtils import color_embed, success_embed, error_embed
from src.utils.formatUtils import format_coins, rarity_emoji

data_file = 'src/data/userData.json'


def standalone_commands():
    # TODO add buttons to the report message for warn and mute (no kick or ban because misclicks are possible)
    @bot.tree.context_menu(name='Report Message')
    async def report_message(
            interaction: discord.Interaction, message: discord.Message
    ):
        interaction.response.defer()

        report_channel = getData(
            'src/data/serverData.json', interaction.guild_id, 'report_channel'
        )
        if report_channel:
            fields = [
                ('Reported By', interaction.user.mention, True),
                ('Message', f'[Jump to message]({message.jump_url})', True),
            ]

            await error_embed(
                interaction,
                title='Message Reported',
                message=f'{message.content}\n-# sent by {message.author.mention}',
                fields=fields,
                channel=report_channel,
            )
            await interaction.response.send_message(
                'Thank you for your report', ephemeral=True
            )
        else:
            await error_embed(
                interaction,
                title='Report Channel Not Set',
                message='The report channel has not yet been set',
            )

    # TODO add buttons to the report message for warn and mute (no kick or ban because misclicks are possible)
    @bot.tree.context_menu(name='Report User')
    async def report_user(interaction: Interaction, user: discord.User):
        await interaction.response.defer()

        report_channel = getData(
            'src/data/serverData.json', interaction.guild_id, 'report_channel'
        )
        if report_channel:
            fields = [
                ('Reported By', interaction.user.mention, True),
                ('Reported User', user.mention, True),
            ]

            await error_embed(
                interaction,
                title='User Reported',
                fields=fields,
                channel=report_channel,
            )
            await interaction.response.send_message(
                'Thank you for your report', ephemeral=True
            )
        else:
            await error_embed(
                interaction,
                title='Report channel not set',
                message='The report channel has not yet been set',
            )

    @bot.tree.context_menu(name='Get Linked Account')
    async def get_linked_account(interaction: Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=True)
        #        linked_users = loadData('src/data/userData.json')
        #        linked_account = linked_users.get(str(user.id), None)
        dtb = UserDataAdapter()
        linked_account = dtb.get_user(user_id=user.id)

        if linked_account[3] is not None:
            username = get_username_from_uuid(linked_account[3])
            await interaction.edit_original_response(
                content=f"{user.name}'s linked Minecraft account: `{username}`"
            )
        else:
            await interaction.edit_original_response(
                content=f'{user.name} has not linked their Minecraft account.'
            )
        dtb.close()

    # TODO change /link from storing guild, to storing guild id
    @bot.tree.command(
        name='link', description='Link your Discord ID with your Minecraft username'
    )
    @app_commands.describe(username='Your Minecraft username')
    async def link(interaction: discord.Interaction, username: str = None):
        await interaction.response.defer()

        user_id = str(interaction.user.id)
        discord_username = str(interaction.user)

        success, uuid, guild_name, error_message = linkMinecraftAccount(
            minecraft_username=username,
            hypixel_api_key=api_key,
            discord_user_id=user_id,
            discord_username=discord_username,
        )

        if success:
            dtb = UserDataAdapter()
            dtb.update_user(
                user_id=interaction.user.id,
                minecraft_uuid=uuid,
                guild=guild_name

            )
            if guild_name:
                await success_embed(
                    interaction,
                    title='Linked Successfully!',
                    message=f'Linked your Discord account to **{username}** in the guild **{guild_name}**',
                )
            else:
                await success_embed(
                    interaction,
                    title='Linked Successfully!',
                    message=f'Linked your Discord account to **{username}**, but guild link was unsuccessful',
                )
            dtb.close()
        else:
            await error_embed(
                interaction,
                title='Link Unsuccessful',
                message=error_message,
            )

    @bot.tree.command(
        name='unlink', description='Unlink your Minecraft username and guild'
    )
    async def unlink(interaction: discord.Interaction):
        await interaction.response.defer()

        dtb = UserDataAdapter()

        user = dtb.get_user(user_id=interaction.user.id)

        if user[3] is None:
            await error_embed(
                interaction,
                title='Unlink Unsuccessful',
                message='Your account is not linked to any username',
            )
            return

        dtb.unlink_user(
            user_id=interaction.user.id,
        )

        await success_embed(
            interaction,
            title='Unlinked Successfully!',
            message='Unlinked your Minecraft username and guild from your Discord account.',
        )
        dtb.close()

    @bot.tree.command(name='uptime', description='Get the uptime of a Minecraft player')
    @app_commands.describe(username='Your Minecraft username')
    async def uptime(interaction: Interaction, username: str = None):
        await interaction.response.defer()

        if username is None:
            dtb = UserDataAdapter()
            username = dtb.get_user(user_id=interaction.user.id)[3]
            if username is None or username == '':
                await error_embed(
                    interaction,
                    title='No linked account!',
                    message='You have not linked your Minecraft account with `/link` yet.',
                )
                return
            dtb.close()
        else:
            username = get_mojang_uuid(username)

        await get_uptime(interaction, username)

    @bot.tree.command(name='color', description='Set your preferred color')
    @app_commands.describe(
        color='The color you want to set (in hexadecimal format, e.g., #3498db)'
    )
    async def set_color(interaction: Interaction, color: str):
        user_id = interaction.user.id
        dtb = UserDataAdapter()
        try:
            preferred_color = color.replace('#', '')[
                              :6
                              ]  # removes all # characters from the hex code
            int(preferred_color, 16)  # convert from hex to integer
        except ValueError:
            await interaction.response.send_message(
                'Invalid color format. Please use hexadecimal format (e.g., #3498db)',
                ephemeral=True,
            )
            return

        if dtb.get_user(user_id) is None:
            dtb.insert_user(user_id=user_id, preferred_color=preferred_color)
        else:
            dtb.update_user(user_id=user_id, preferred_color=preferred_color)

        color = dtb.get_user(user_id)[1]
        color = int(color, 16)

        role = await create_role(
            interaction.guild, name=interaction.user.display_name, color=color
        )
        if role is None:
            await color_embed(
                interaction, f'Your user color has been set to #{preferred_color}'
            )

        await interaction.user.add_roles(role)

        embed = discord.Embed(
            title='',
            description=f'Your user color has been set to #{preferred_color}',
            color=color,
        )
        await interaction.response.send_message(embed=embed)

    # TODO create view to switch from insta sell to sell order (sell order by default)
    # DO NOT TOUCH UNLESS YOU KNOW WHAT YOU'RE DOING
    @bot.tree.command(
        name='bits', description='Calculate the best items to buy with your bits'
    )
    async def bits(interaction: Interaction):
        try:
            await interaction.response.defer()

            bz_items = loadData('src/data/bits/bzItems.json')
            ah_items = loadData('src/data/bits/ahItems.json')
            results = []

            for item_id, item_info in bz_items.items():
                selloffer = item_info.get('selloffer')
                bits = item_info.get('bits')
                name = item_info.get('name', 'item name not found!')
                emoji = item_info.get('emoji', '❓')
                if selloffer and bits:
                    ratio = selloffer / bits
                    results.append((f'{emoji} {name}', ratio, bits, selloffer))

            for item_name, item_info in ah_items.items():
                lowest_bin = item_info.get('lowest_bin')
                bits = item_info.get('bits')
                name = item_info.get('name', item_name)
                emoji = item_info.get('emoji', '❓')
                if lowest_bin and bits:
                    ratio = lowest_bin / bits
                    results.append((f'{emoji} {name}', ratio, bits, lowest_bin))

            results.sort(key=lambda x: x[1], reverse=True)

            view = BitsView(results, interaction)

            user_id = str(interaction.user.id)
            color = getData('src/data/userData.json', user_id, 'preferred_color')
            if color is None:
                color = int('36393F', 16)
            else:
                color = int(color, 16)

            embed = discord.Embed(description=view.get_page_content(), color=color)
            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            await interaction.followup.send(f'An error occurred: {e}')

    @bot.tree.command(
        name='petflip', description='Find the best pets to exp share for money'
    )
    @app_commands.choices(type=pet_types)
    async def petflip(interaction: Interaction, type: str = None):
        await interaction.response.defer()
        # farming =

        await color_embed(interaction, message=f'welcome to the goon cave')

    @bot.tree.command(name='test')
    async def test(interaction: Interaction):
        await interaction.response.send_message(
            'im not testing anything right now! <a:snivypet:1287698450812506165>'
        )


class Admin(app_commands.Group):
    """@app_commands.command(name='delete_role')
    @commands.has_permissions(administrator=True)
    async def delete_role(interaction: Interaction, role: str):
        await role.delete()
        await success_embed(interaction, message=f'Deleted role {role.name}')"""


from discord.errors import NotFound


class Setup(app_commands.Group):
    @app_commands.command(
        name='report_channel', description='Set the channel for reports to go to'
    )
    @commands.has_permissions(administrator=True)
    async def set_report_channel(self, interaction: Interaction):
        await interaction.response.defer()

        saveLibraryData(
            'src/data/serverData.json',
            str(interaction.guild_id),
            'report_channel',
            interaction.channel_id,
        )

        try:
            await success_embed(
                interaction,
                message=f'Set the report channel to <#{interaction.channel_id}>',
            )
        except NotFound:
            await interaction.followup.send(
                'Failed to send success message: Unknown Webhook', ephemeral=True
            )

    @app_commands.command(
        name='admin_role', description='Set the admin role for the server'
    )
    @app_commands.describe(role='Ping the role you want to set as admin')
    @commands.has_permissions(administrator=True)
    async def set_admin_role(self, interaction: Interaction, role: discord.Role):
        await interaction.response.defer()

        saveLibraryData(
            'src/data/serverData.json', interaction.guild_id, 'admin_role', role.id
        )

        try:
            await success_embed(
                interaction, message=f'Set the admin role to {role.mention}'
            )
        except NotFound:
            await interaction.followup.send(
                'Failed to send success message: Unknown Webhook', ephemeral=True
            )


class Guild(app_commands.Group):
    @app_commands.command(name='xp', description='Top 10 players in guild xp this week')
    async def xp(self, interaction: discord.Interaction, guild: str = None):
        if guild is None:
            guild = getData(data_file, str(interaction.user.id), 'guild')
            if guild is None or guild == '':
                await error_embed(
                    interaction,
                    title='No linked guild!',
                    message='You have not linked your Hypixel guild with `/link` yet.',
                )
                return

        await guild_leaderboard(interaction, guild_name=guild)

    @app_commands.command(
        name='uptime', description='Get the uptime leaderboard for a guild'
    )
    async def guild_uptime(self, interaction: Interaction, guild: str = None):
        if guild is None:
            guild = getData(data_file, str(interaction.user.id), 'guild')
            if guild is None or guild == '':
                await error_embed(
                    interaction,
                    title='No linked account!',
                    message='You have not linked your Minecraft account with `/link` yet.',
                )
                return

        await guild_uptime(interaction, guild)
