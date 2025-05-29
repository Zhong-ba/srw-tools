import json

CONFIG = None

with open('scriptconfig.json', 'r', encoding = 'utf-8') as file:
    CONFIG = json.load(file)