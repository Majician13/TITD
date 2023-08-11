import json

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data
