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


#TODO for both saveLibraryData and getData, parse key so that you can like input key1/key2/key3.... to get nested data
#TODO change /link from storing guild, to storing guild id
def saveLibraryData(file_path, key, data_type, data):
    key = str(key)
    json_data = loadData(file_path)

    if key not in json_data:
        json_data[key] = {}

    json_data[key][data_type] = data

    saveData(file_path, json_data)


def getData(file_path, key, data_type):
    key = str(key)
    json_data = loadData(file_path)

    if key in json_data and data_type in json_data[key]:
        return json_data[key][data_type]
    else:
        return None
