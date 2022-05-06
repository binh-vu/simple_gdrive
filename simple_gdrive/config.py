from typing import List, Optional
from os.path import expanduser


class Config:
    SCOPES: List[str] = ["https://www.googleapis.com/auth/drive.readonly"]
    AUTH_DIR: str = expanduser("~/.simple_gdrive")
    TokenFileName: str = "token.json"
    CredentialFileName: str = "credentials.json"
