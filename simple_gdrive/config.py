import os
from typing import List, Optional
from os.path import expanduser, join
from enum import Enum


class Scope(str, Enum):
    # for all scopes, see: https://developers.google.com/identity/protocols/oauth2/scopes#drive
    all = "https://www.googleapis.com/auth/drive"
    readonly = "https://www.googleapis.com/auth/drive.readonly"


class Config:
    AuthDir: str = expanduser("~/.simple_gdrive")

    TokenFileName: str = "token.json"
    CredentialFileName: str = "credentials.json"

    @staticmethod
    def get_token_file(scope: Scope) -> str:
        return join(Config.AuthDir, scope.name, Config.TokenFileName)

    @staticmethod
    def get_credential_file(scope: Scope) -> str:
        return join(Config.AuthDir, Config.CredentialFileName)

    @staticmethod
    def get_available_scope() -> Optional[Scope]:
        for scope in [Scope.all, Scope.readonly]:
            if os.path.exists(os.path.join(Config.AuthDir, scope)):
                return scope
        return None
