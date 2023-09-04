from .base import DTO


class TokenData(DTO):
    access_token: str
    token_type: str = 'Bearer'
