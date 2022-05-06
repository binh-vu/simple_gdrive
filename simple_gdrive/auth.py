import os
from simple_gdrive.config import Config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def auth():
    """Authenticate with Google Drive, save the tokens to the file for future uses.

    The code is borrow from here: https://developers.google.com/drive/api/quickstart/python.

    Returns: the credentials object.
    """
    creds = None

    scopes = Config.SCOPES
    token_file = os.path.join(Config.AUTH_DIR, Config.TokenFileName)
    credential_file = os.path.join(Config.AUTH_DIR, Config.CredentialFileName)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds


def service():
    return
