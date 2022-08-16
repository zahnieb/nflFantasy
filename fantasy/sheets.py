import fantasy.requester as requester
from googleapiclient.errors import HttpError


def get_values(spreadsheet_id, range_name):
    #load pre-authorized credentials from environment.
    creds, _ = requester.google.auth.default()

    try:
        service = requester.build('sheets', 'v4', credentials = creds)

        result = service.spreadsheets().values().get(
            spreadsheetId = spreadsheet_id, range = range_name).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retreived")
        return result
    except HttpError as error:
        print(f"An error has occurred: {error}")
        return error

def update_values(spreadsheet_id, range_name, value_input_option, _values):
    #loads pre-authorized user creds from environment
    #creates batch_updates user has access to
    creds, _ = requester.google.auth.default()

    try:
        service = requester.build('sheets', 'v4', credentials = creds)
        values = _values
        body = {
            'values':values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId = spreadsheet_id, range = range_name,
            valueInputOption = value_input_option, body = body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f'An error occurred: {error}')
        return error

def print_index_table():
    return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')