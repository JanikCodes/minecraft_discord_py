import json

botConfig = None

# load bot token from json
with open('bot.json') as file:
    botConfig = json.load(file)
