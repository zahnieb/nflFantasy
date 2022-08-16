import flask
import fantasy.requester as requester
import requests
import os
from dotenv import load_dotenv
import fantasy.sheets as sheets
from fantasy import app


SPORTSDATA_KEY = os.getenv('SPORTSDATA_KEY')
#google sheet api constants
SHEETS_KEY = os.getenv('SHEET_KEY')
SHEETS_ID = os.getenv('SHEET_ID')
SHEETS_SECRET = os.getenv('SHEET_SECRET')
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/top100")
def player():
    headers = {
        'Ocp-Apim-Subscription-Key': f'{SPORTSDATA_KEY}'
    }

    playersListURL = f'https://api.sportsdata.io/v3/nfl/scores/json/Players'
    
    #request to api
    requestPlayer = requests.get(playersListURL, headers = headers)
    json_dataPlayer = requestPlayer.json()
    data = json_dataPlayer
    playerData = []

    #return data of top 100 avg draft position player, NOT sorted/formatted
    for data in json_dataPlayer:
        tempDraft = data['AverageDraftPosition']
        if tempDraft == None or int(tempDraft) > 100:
            continue
        arrResult = [data['Name'],data['AverageDraftPosition']]
        #name = data['Name']
        #averageDraftPos = data['AverageDraftPosition']
        playerData.append(arrResult)

    #sort by lowest -> highest average draft position
    playerData.sort(key = lambda x: x[1])

    return playerData

@app.route("/top100toSheet")
def playerSheet():
    headers = {
        'Ocp-Apim-Subscription-Key': f'{SPORTSDATA_KEY}'
    }

    playersListURL = f'https://api.sportsdata.io/v3/nfl/scores/json/Players'
    
    #request to api
    requestPlayer = requests.get(playersListURL, headers = headers)
    json_dataPlayer = requestPlayer.json()
    data = json_dataPlayer
    playerData = []

    #return data of top 100 avg draft position player, NOT sorted/formatted
    for data in json_dataPlayer:
        tempDraft = data['AverageDraftPosition']
        if tempDraft == None or int(tempDraft) > 100:
            continue
        arrResult = [data['Name'],data['AverageDraftPosition']]
        #name = data['Name']
        #averageDraftPos = data['AverageDraftPosition']
        playerData.append(arrResult)

    #sort by lowest -> highest average draft position
    playerData.sort(key = lambda x: x[1])

    ##write top 100 to excel sheet
    FANTASY_SHEET_ID = os.getenv('FANTASY_SHEET_ID')
    range = f"A2:B160"
    enterType = "USER_ENTERED" #other types are RAW & INPUT_VALUE_OPTION_UNSECIFIED
    input_values = playerData

    requester.requesterG()

    sheets.update_values(FANTASY_SHEET_ID, range, enterType, input_values)

    return playerData

    ##08/08/2022 create oauth with goggle to WRITE data from sportsdata.io api
    #

@app.route('/authorize')
def authorize():
    #flow to manage oauth2.0 authorization grant steps.
    env = load_dotenv()
    flow = requester.google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
     scopes = SCOPES)

    #URI must match authorized redirect URIs for oauth 2.0 client configured in API console.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        #enable offline access to refresh token w/o re-prompting user perms.
        access_type = 'offline',
        #enable incremental authorization. recommended best practice.
        include_granted_scopes='true')

    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    #specify state when creating flow in callback to verify the authorization server response
    state = flask.session['state']

    flow = requester.google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes = SCOPES,
     state = state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    #use authorization server's response to fetch oauth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    #store credentials in session.
    credentials = flow.credentials
    flask.session['credentials'] = requester.credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('sheet'))

@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
        'testing the code to revoke credentials.')
    
    credentials = requester.google.oauth2.credentials.Credentials(**flask.session['credentials'])

    revoke = requester.requests.port('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.' + sheets.print_index_table())
    else:
        return('An error occurred.' + sheets.print_index_table())

@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleard.<br><br>' + sheets.print_index_table())

@app.route('/sheet')
def sheet():
    FANTASY_SHEET_ID = os.getenv('FANTASY_SHEET_ID')
    range = "Sheet1!A1:B2"
    creds = None

    requester.requesterG()

    #return google sheet values from range
    return sheets.get_values(FANTASY_SHEET_ID, range)

@app.route('/write')
def write():
    FANTASY_SHEET_ID = os.getenv('FANTASY_SHEET_ID')
    range = "A2:B101"
    enterType = "USER_ENTERED" #other types are RAW & INPUT_VALUE_OPTION_UNSECIFIED
    input_values = [['A','B'],['C','D']]
    creds = None

    requester.requesterG()

    return sheets.update_values(FANTASY_SHEET_ID, range, enterType, input_values)

