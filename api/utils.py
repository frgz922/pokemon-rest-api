import json


def read_json(path):
    with open(path) as f:
        json_data = json.loads(f.read())
    
    return json_data