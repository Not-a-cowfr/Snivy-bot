import json

from startBot import logger

from src.utils.jsonDataUtils import loadData, saveData
from src.utils.playerUtils import get_online_status, get_mojang_uuid


def add_tracker(username: str, user_id: str, file_path: str = 'src/data/tracked_players.json'):
    try:
        tracked_players = loadData(file_path)
    except FileNotFoundError:
        logger.error('Tracked players file not found')
        return

    # check if player exists
    uuid, error = get_mojang_uuid(username)
    if error:
        logger.info(f'Error fetching UUID for {username}: {error}')
        return 'username_not_found'

    # check if the user is already tracking the player, if so, return error
    if username in tracked_players and user_id in tracked_players[username]['trackers']:
        logger.info(f'User {user_id} is already tracking {username}')
        return 'already_tracking'

    # check if the user is tracking more than 10 players, if so, return error
    user_tracked_count = sum(user_id in data['trackers'] for data in tracked_players.values())
    if user_tracked_count >= 10:
        logger.info(f'User {user_id} is already tracking 10 players')
        return 'max_tracking'

    uuid, error = get_mojang_uuid(username)
    if error:
        logger.error(f'Error fetching UUID for {username}: {error}')
        status = None
    else:
        status = get_online_status(uuid)
        if isinstance(status, str):
            logger.error(f'Error fetching online status for {username}: {status}')
            status = None

    if username in tracked_players:
        tracked_players[username]['trackers'].append(user_id)
    else:
        tracked_players[username] = {
            'trackers': [user_id],
            'status': status
        }

    saveData(file_path, tracked_players)

def remove_tracker(username: str, user_id: str, file_path: str = 'src/data/tracked_players.json'):
    try:
        tracked_players = loadData(file_path)
    except FileNotFoundError:
        logger.error('Tracked players file not found')
        return

    if username not in tracked_players or user_id not in tracked_players[username]['trackers']:
        logger.info(f'User {user_id} is not tracking {username}')
        return 'not_tracking'

    if username in tracked_players:
        if user_id in tracked_players[username]['trackers']:
            tracked_players[username]['trackers'].remove(user_id)
            if not tracked_players[username]['trackers']:
                del tracked_players[username]

    saveData(file_path, tracked_players)

def get_tracked_players(user_id: str, file_path: str = 'src/data/tracked_players.json'):
    try:
        tracked_players = loadData(file_path)
    except FileNotFoundError:
        logger.error('Tracked players file not found')
        return

    user_tracked_players = [
        username for username, data in tracked_players.items() if user_id in data['trackers']
    ]
    return user_tracked_players

def clear_all_trackers(user_id: str, file_path: str = 'src/data/tracked_players.json'):
    try:
        tracked_players = loadData(file_path)
    except FileNotFoundError:
        logger.error('Tracked players file not found')
        return

    user_tracked_any = False
    for username, data in list(tracked_players.items()):
        if user_id in data['trackers']:
            user_tracked_any = True
            data['trackers'].remove(user_id)
            if not data['trackers']:
                del tracked_players[username]

    if not user_tracked_any:
        return 'not_tracking_any'

    saveData(file_path, tracked_players)
    return 'success'
