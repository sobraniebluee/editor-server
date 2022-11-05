from typing import Dict


class SettingsT(Dict):
    live_mode: bool
    password: str
    read_only: bool


class OAuthData(Dict):
    login: str
    id: str
    avatar: str
    access_token: str
