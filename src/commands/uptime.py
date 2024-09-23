import requests
import discord

from botSetup import bot, api_key

from src.utils.embedUtils import color_embed, error_embed
from src.utils.playerUtils import get_mojang_uuid, get_hypixel_guild_data, get_guild_members,get_hypixel_guild_data_by_guild, get_username_from_uuid
from src.utils.jsonDataUtils import loadData, getData

#TODO change /link from storing guild, to storing guild id
async def uptime(interaction: discord.Interaction, player_name: str):
    await interaction.response.defer()  # Defer the interaction response

    user_id = str(interaction.user.id)
    linked_users = loadData('src/data/userData.json')

    if user_id not in linked_users:
        linked_users[user_id] = {}
    elif isinstance(linked_users[user_id], str):
        linked_users[user_id] = {'username': linked_users[user_id]}

    player_uuid, error_message = get_mojang_uuid(player_name)
    if error_message:
        await error_embed(interaction, title='Error', message=error_message)
        return

    if player_uuid:
        guild_data = get_hypixel_guild_data(api_key, player_uuid)
        if isinstance(guild_data, str):
            await error_embed(interaction, message=guild_data, title='Error')
            return

        if player_uuid == '3280f05b402a4716be8fb40185aac2ae': # ily pklm
            guild_data = {date: f"{int(uptime.split(':')[0]) * 2}:{uptime.split(':')[1]}" for date, uptime in guild_data.items()}

        # i feel like this could be optimized but i cba to do that
        total_exp = sum(int(uptime.split(':')[0]) * 9000 + int(uptime.split(':')[1]) * 150 for uptime in guild_data.values())
        total_hours = total_exp // 9000
        total_minutes = (total_exp % 9000) / 150
        avg_exp_per_day = total_exp / 7
        avg_hours = avg_exp_per_day // 9000
        avg_minutes = (avg_exp_per_day % 9000) / 150
        hour_label = "hour" if total_hours == 1 else "hours"
        minute_label = "minute" if total_minutes == 1 else "minutes"
        avg_hour_label = "hour" if avg_hours == 1 else "hours"
        avg_minute_label = "minute" if avg_minutes == 1 else "minutes"

        description_lines = []
        for date, uptime in guild_data.items():
            hours, minutes = uptime.split(':')
            hours = int(hours)
            minutes = int(minutes)
            day_hour_label = "hour" if hours == 1 else "hours"
            day_minute_label = "minute" if minutes == 1 else "minutes"
            description_lines.append(f"**{date}**: {hours} {day_hour_label} | {minutes} {day_minute_label}")

        description_lines.append(f"\nTotal uptime for the week: **{total_hours}** {hour_label}  **{round(total_minutes)}** {minute_label}")
        description_lines.append(f"Average uptime per day: **{int(avg_hours)}** {avg_hour_label}  **{round(avg_minutes)}** {avg_minute_label}")

        description = "\n".join(description_lines)
        await color_embed(interaction, title=f'Uptime for {player_name}', message=description)
    else:
        await error_embed(interaction, message='Player not found', title='Error')


