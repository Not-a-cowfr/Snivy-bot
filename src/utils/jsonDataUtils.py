import json


def loadData(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON data: {e}")
        return {}


def saveData(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def saveUserData(file_path, user_id, data_type, data):
    user_id = str(user_id)
    json_data = loadData(file_path)

    if user_id not in json_data:
        json_data[user_id] = {}

    json_data[user_id][data_type] = data

    saveData(file_path, json_data)

def getData(file_path, user_id, data_type):
    user_id = str(user_id)
    json_data = loadData(file_path)

    if user_id in json_data and data_type in json_data[user_id]:
        return json_data[user_id][data_type]
    return None
