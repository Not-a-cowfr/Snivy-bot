import json
import logging
import discord
from discord.ext import tasks
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from src.utils.jsonDataUtils import loadData, saveData
from src.utils.playerUtils import get_online_status, get_mojang_uuid

logger = logging.getLogger('my_app')

# Load the bot instance from botSetup
from botSetup import bot

@tasks.loop(minutes=5)
async def check_player_status():
    file_path = 'src/data/tracked_players.json'
    try:
        tracked_players = loadData(file_path)
    except FileNotFoundError:
        logger.error('Tracked players file not found')
        return

    total_players = len(tracked_players)
    with logging_redirect_tqdm():
        with tqdm(total=total_players, desc="Fetching tracked players status", bar_format="{desc}: {percentage:3.0f}%|{bar}| player {n_fmt}/{total_fmt}, [{rate_fmt}]") as pbar:
            for username, data in tracked_players.items():
                uuid_tuple = get_mojang_uuid(username)
                uuid = uuid_tuple[0] if uuid_tuple else None
                if not uuid:
                    logger.error(f'UUID not found for {username}')
                    pbar.update(1)
                    continue

                current_status = get_online_status(uuid)
                saved_status = data.get('status')

                if current_status != saved_status and saved_status is not None:
                    for user_id in data['trackers']:
                        user = await bot.fetch_user(user_id)
                        if user:
                            try:
                                embed = discord.Embed(
                                    title=f'{username} is now {"online" if current_status else "offline"}',
                                    description='',
                                    color=discord.Color.green() if current_status else discord.Color.red()
                                )
                                await user.send(embed=embed)
                                logger.info(f'{username}\'s status has changed, dm has been sent to user {user_id}')
                            except discord.Forbidden:
                                logger.error(f'Cannot send DM to user {user_id}')
                    data['status'] = current_status

                pbar.update(1)

    saveData(file_path, tracked_players)

@check_player_status.before_loop
async def before_check_player_status():
    await bot.wait_until_ready()