import flask
from google.auth.transport.requests import Request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import build

import os
from dotenv import load_dotenv

SPORTSDATA_KEY = os.getenv('SPORTSDATA_KEY')
#google sheet api constants
SHEETS_KEY = os.getenv('SHEET_KEY')
SHEETS_ID = os.getenv('SHEET_ID')
SHEETS_SECRET = os.getenv('SHEET_SECRET')
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'

def requesterG():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')
    
    #load credentials from session.
    credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])

    drive = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

    #save creds back to session in case access token refreshed.
    flask.session['credentials'] = credentials_to_dict(credentials)

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
            }

