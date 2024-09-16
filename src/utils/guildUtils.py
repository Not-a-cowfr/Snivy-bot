import requests


def get_mojang_uuid(player_name):
    if not player_name:
        return None, "You have not linked your Minecraft account yet."

    url = f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("id"), None
    else:
        return None, f"Error fetching UUID: {response.status_code}"


def get_username_from_uuid(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "name" in data:
            return data["name"]
        else:
            return "No username found for this UUID."
    elif response.status_code == 404:
        return "Username not found (UUID may be invalid)."
    else:
        return f"Error fetching username: {response.status_code}"


def get_hypixel_guild_data(api_key, player_uuid):
    url = "https://api.hypixel.net/guild"
    params = {
        "key": api_key,
        "player": player_uuid
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            guild = data.get("guild")
            exp_history = None
            for member in guild.get("members", []):
                if member.get("uuid") == player_uuid:
                    exp_history = member.get("expHistory")
                    break
            if exp_history:
                formatted_exp_history = {}
                for date, exp in exp_history.items():
                    hours = exp // 9000
                    minutes = (exp % 9000) / 150
                    formatted_exp_history[date] = f"{hours}:{round(minutes)}"
                return formatted_exp_history
            else:
                return "Player UUID not found in guild members."
        else:
            return f"Error: {data.get('cause')}"
    else:
        return f"HTTP Error: {response.status_code}"

#TODO replace with get guild data by id
def get_hypixel_guild_data_by_guild(api_key, guild_name):
    url = "https://api.hypixel.net/guild"
    params = {
        "key": api_key,
        "name": guild_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("guild")
        else:
            return f"Error: {data.get('cause')}"
    else:
        return f"HTTP Error: {response.status_code}"
