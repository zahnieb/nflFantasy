#Fantasy players data retrieval and sorting from fantasydata.com
from tokenize import Double
import requests
import json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    
@app.route("/top100")
def player():
    with open('keys.json') as file:
        data = json.load(file)
    key = data['key']

    headers = {
        'Ocp-Apim-Subscription-Key': f'{key}'
    }

    season = 2022
    playerid = 18890

    playerURL = f'https://api.sportsdata.io/v3/nfl/projections/json/PlayerSeasonProjectionStatsByPlayerID/{season}/{playerid}'
    playersListURL = f'https://api.sportsdata.io/v3/nfl/scores/json/Players'
    #request to api 
    r = requests.get(playerURL, headers = headers)
    requestPlayer = requests.get(playersListURL, headers = headers)
    #json_data = r.json() if r and r.status_code == 200 else None
    json_dataPlayer = requestPlayer.json()
    data = json_dataPlayer
    name = ''
    averageDraftPos = ''
    playerData = ''

    #return data of top 100 avg draft position player, NOT sorted/formatted
    for data in json_dataPlayer:
        tempDraft = data['AverageDraftPosition']
        if tempDraft == None or int(tempDraft) > 100:
            continue
        name = data['Name']
        averageDraftPos = data['AverageDraftPosition']
        playerData = f'{name} {averageDraftPos}' + playerData

    return playerData
        
    ##08/08/2022 create oauth with goggle to READ data from google spreadsheet
    ##make route/auth that accepts a query parameter of google that will try 
    # to authenticate with google
    #Exame route: http://localhost:3000/auth?google%60


@app.route('/spreadsheet')
def googleSheet():

    test = "hello"
    return test
 
 
