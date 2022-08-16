from flask import Flask
import os
from dotenv import load_dotenv

    
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

import fantasy.views

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPS verification.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Specify a hostname and port that are set as a valid redirect URI
# for your API project in the Google API Console.
    app.run('localhost', 5000, debug=True)
