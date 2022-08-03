import requests
import json


with open('keys.json') as file:
    data = json.load(file)
key = data['key']

headers = {
    'Ocp-Apim-Subscription-Key': f'{key}'
}

season = 2022
playerid = 18890

url = f'https://api.sportsdata.io/v3/nfl/projections/json/PlayerSeasonProjectionStatsByPlayerID/{season}/{playerid}'

r = requests.get(url, headers = headers)

info = r.json()

print(info)