# #Fantasy players data retrieval and sorting from fantasydata.com
# from __future__ import print_function
# from distutils.log import error
# from email import header
# import os
# from dotenv import load_dotenv
# from tokenize import Double
# import requests
# import json
# import flask
# from flask import Flask
# from flask_session import Session
# #google API imports
# from google.auth.transport.requests import Request
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from flask import Flask
# import os
# from dotenv import load_dotenv
    
# app = Flask(__name__)
# app.secret_key = os.getenv('FLASK_SECRET')



# SPORTSDATA_KEY = os.getenv('SPORTSDATA_KEY')
# #google sheet api constants
# SHEETS_KEY = os.getenv('SHEET_KEY')
# SHEETS_ID = os.getenv('SHEET_ID')
# SHEETS_SECRET = os.getenv('SHEET_SECRET')
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# API_SERVICE_NAME = 'drive'
# API_VERSION = 'v2'
# CLIENT_SECRETS_FILE = 'client_secret.json'

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/top100")
# def player():
#     headers = {
#         'Ocp-Apim-Subscription-Key': f'{SPORTSDATA_KEY}'
#     }

#     playersListURL = f'https://api.sportsdata.io/v3/nfl/scores/json/Players'
    
#     #request to api
#     requestPlayer = requests.get(playersListURL, headers = headers)
#     json_dataPlayer = requestPlayer.json()
#     data = json_dataPlayer
#     playerData = []

#     #return data of top 100 avg draft position player, NOT sorted/formatted
#     for data in json_dataPlayer:
#         tempDraft = data['AverageDraftPosition']
#         if tempDraft == None or int(tempDraft) > 100:
#             continue
#         arrResult = [data['Name'],data['AverageDraftPosition']]
#         #name = data['Name']
#         #averageDraftPos = data['AverageDraftPosition']
#         playerData.append(arrResult)

#     #sort by lowest -> highest average draft position
#     playerData.sort(key = lambda x: x[1])

#     return playerData

# @app.route("/top100toSheet")
# def playerSheet():
#     headers = {
#         'Ocp-Apim-Subscription-Key': f'{SPORTSDATA_KEY}'
#     }

#     playersListURL = f'https://api.sportsdata.io/v3/nfl/scores/json/Players'
    
#     #request to api
#     requestPlayer = requests.get(playersListURL, headers = headers)
#     json_dataPlayer = requestPlayer.json()
#     data = json_dataPlayer
#     playerData = []

#     #return data of top 100 avg draft position player, NOT sorted/formatted
#     for data in json_dataPlayer:
#         tempDraft = data['AverageDraftPosition']
#         if tempDraft == None or int(tempDraft) > 100:
#             continue
#         arrResult = [data['Name'],data['AverageDraftPosition']]
#         #name = data['Name']
#         #averageDraftPos = data['AverageDraftPosition']
#         playerData.append(arrResult)

#     #sort by lowest -> highest average draft position
#     playerData.sort(key = lambda x: x[1])

#     ##write top 100 to excel sheet
#     FANTASY_SHEET_ID = os.getenv('FANTASY_SHEET_ID')
#     range = f"A2:B160"
#     enterType = "USER_ENTERED" #other types are RAW & INPUT_VALUE_OPTION_UNSECIFIED
#     input_values = playerData

#     requesterG()

#     update_values(FANTASY_SHEET_ID, range, enterType, input_values)

#     return playerData

#     ##08/08/2022 create oauth with goggle to WRITE data from sportsdata.io api
#     #

# @app.route('/authorize')
# def authorize():
#     #flow to manage oauth2.0 authorization grant steps.
#     env = load_dotenv()
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
#      scopes = SCOPES)

#     #URI must match authorized redirect URIs for oauth 2.0 client configured in API console.
#     flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

#     authorization_url, state = flow.authorization_url(
#         #enable offline access to refresh token w/o re-prompting user perms.
#         access_type = 'offline',
#         #enable incremental authorization. recommended best practice.
#         include_granted_scopes='true')

#     flask.session['state'] = state

#     return flask.redirect(authorization_url)

# @app.route('/oauth2callback')
# def oauth2callback():
#     #specify state when creating flow in callback to verify the authorization server response
#     state = flask.session['state']

#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes = SCOPES,
#      state = state)
#     flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

#     #use authorization server's response to fetch oauth 2.0 tokens.
#     authorization_response = flask.request.url
#     flow.fetch_token(authorization_response=authorization_response)

#     #store credentials in session.
#     credentials = flow.credentials
#     flask.session['credentials'] = credentials_to_dict(credentials)

#     return flask.redirect(flask.url_for('sheet'))

# @app.route('/revoke')
# def revoke():
#     if 'credentials' not in flask.session:
#         return ('You need to <a href="/authorize">authorize</a> before ' +
#         'testing the code to revoke credentials.')
    
#     credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])

#     revoke = requests.port('https://oauth2.googleapis.com/revoke',
#       params={'token': credentials.token},
#       headers = {'content-type': 'application/x-www-form-urlencoded'})

#     status_code = getattr(revoke, 'status_code')
#     if status_code == 200:
#         return('Credentials successfully revoked.' + print_index_table())
#     else:
#         return('An error occurred.' + print_index_table())

# @app.route('/clear')
# def clear_credentials():
#     if 'credentials' in flask.session:
#         del flask.session['credentials']
#     return ('Credentials have been cleard.<br><br>' + print_index_table())

# @app.route('/sheet')
# def sheet():
#     FANTASY_SHEET_ID = os.getenv('FANTASY_SHEET_ID')
#     range = "Sheet1!A1:B2"
#     creds = None

#     requesterG()

#     #return google sheet values from range
#     return get_values(FANTASY_SHEET_ID, range)

# @app.route('/write')
# def write():
#     FANTASY_SHEET_ID = os.getenv('FANTASY_SHEET_ID')
#     range = "A2:B101"
#     enterType = "USER_ENTERED" #other types are RAW & INPUT_VALUE_OPTION_UNSECIFIED
#     input_values = [['A','B'],['C','D']]
#     creds = None

#     requesterG()

#     return update_values(FANTASY_SHEET_ID, range, enterType, input_values)

# def credentials_to_dict(credentials):
#     return {'token': credentials.token,
#             'refresh_token': credentials.refresh_token,
#             'token_uri': credentials.token_uri,
#             'client_id': credentials.client_id,
#             'client_secret': credentials.client_secret,
#             'scopes': credentials.scopes
#             }

# def print_index_table():
#     return ('<table>' +
#           '<tr><td><a href="/test">Test an API request</a></td>' +
#           '<td>Submit an API request and see a formatted JSON response. ' +
#           '    Go through the authorization flow if there are no stored ' +
#           '    credentials for the user.</td></tr>' +
#           '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
#           '<td>Go directly to the authorization flow. If there are stored ' +
#           '    credentials, you still might not be prompted to reauthorize ' +
#           '    the application.</td></tr>' +
#           '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
#           '<td>Revoke the access token associated with the current user ' +
#           '    session. After revoking credentials, if you go to the test ' +
#           '    page, you should see an <code>invalid_grant</code> error.' +
#           '</td></tr>' +
#           '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
#           '<td>Clear the access token currently stored in the user session. ' +
#           '    After clearing the token, if you <a href="/test">test the ' +
#           '    API request</a> again, you should go back to the auth flow.' +
#           '</td></tr></table>')

# #use before google API call to verify credentials

# def get_values(spreadsheet_id, range_name):
#     #load pre-authorized credentials from environment.
#     creds, _ = google.auth.default()

#     try:
#         service = build('sheets', 'v4', credentials = creds)

#         result = service.spreadsheets().values().get(
#             spreadsheetId = spreadsheet_id, range = range_name).execute()
#         rows = result.get('values', [])
#         print(f"{len(rows)} rows retreived")
#         return result
#     except HttpError as error:
#         print(f"An error has occurred: {error}")
#         return error

# def update_values(spreadsheet_id, range_name, value_input_option, _values):
#     #loads pre-authorized user creds from environment
#     #creates batch_updates user has access to
#     creds, _ = google.auth.default()

#     try:
#         service = build('sheets', 'v4', credentials = creds)
#         values = _values
#         body = {
#             'values':values
#         }
#         result = service.spreadsheets().values().update(
#             spreadsheetId = spreadsheet_id, range = range_name,
#             valueInputOption = value_input_option, body = body).execute()
#         print(f"{result.get('updatedCells')} cells updated.")
#         return result
#     except HttpError as error:
#         print(f'An error occurred: {error}')
#         return error
    
# if __name__ == '__main__':
#     # When running locally, disable OAuthlib's HTTPS verification.
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#     # Specify a hostname and port that are set as a valid redirect URI
#     # for your API project in the Google API Console.
#     app.run('localhost', 8080, debug=True)
 
 
