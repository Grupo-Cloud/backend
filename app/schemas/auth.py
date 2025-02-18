from pydantic import BaseModel


class OAuth2LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class OAuth2RefreshResponse(BaseModel):
    refresh_token: str
