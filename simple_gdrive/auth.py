from genericpath import exists
import os
from pathlib import Path
from simple_gdrive.config import Config, Scope

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def auth(scope: Scope):
    """Authenticate with Google Drive, save the tokens to the file for future uses.

    The code is borrow from here: https://developers.google.com/drive/api/quickstart/python.

    Returns: the credentials object.
    """
    creds = None

    scopes = [scope.value]
    token_file = Config.get_token_file(scope)
    credential_file = Config.get_credential_file(scope)

    Path(token_file).parent.mkdir(exist_ok=True, parents=True)

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
