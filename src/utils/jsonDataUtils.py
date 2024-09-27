import json


def loadData(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f'Error loading JSON data: {e}')
        return {}


def saveData(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# TODO change /link from storing guild, to storing guild id
def saveLibraryData(file_path, key, data_type, data):
    key = str(key)
    keys = key.split('/')
    json_data = loadData(file_path)

    current_level = json_data
    for k in keys[:-1]:
        if k not in current_level:
            current_level[k] = {}
        current_level = current_level[k]

    if keys[-1] not in current_level:
        current_level[keys[-1]] = {}
    current_level[keys[-1]][data_type] = data

    saveData(file_path, json_data)


def getData(file_path, key, data_type):
    key = str(key)
    keys = key.split('/')
    json_data = loadData(file_path)

    current_level = json_data
    for k in keys:
        if k in current_level:
            current_level = current_level[k]
        else:
            return None

    return current_level.get(data_type)
