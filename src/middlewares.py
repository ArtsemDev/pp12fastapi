from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.authentication import AuthCredentials, BaseUser
from starlette.middleware.authentication import AuthenticationMiddleware, AuthenticationBackend
from starlette.requests import HTTPConnection

from src.database import User
from src.settings import SETTINGS
from src.utils import verify_access_token


class UserInfo(BaseUser):
    def __init__(self, pk: str, email: str):
        self.pk = pk
        self.email = email

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def identity(self) -> str:
        return self.pk

    @property
    def display_role(self) -> str:
        return self.email


class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(
            self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, UserInfo] | None:
        auth = conn.headers.get("Authorization") \
            if 'Authorization' in conn.headers \
            else conn.headers.get("authorization")

        if not auth or not auth.startswith(f"{SETTINGS.TOKEN_TYPE}"):
            return

        token = auth.replace(f"{SETTINGS.TOKEN_TYPE} ", "")

        payload = verify_access_token(token=token)

        if not payload:
            return

        with User.session() as session:  # type: Session
            user: User = session.scalar(
                select(User)
                .filter_by(id=payload.get("sub"))
            )

            if not user:
                return

            return AuthCredentials(["authenticated"]), UserInfo(
                pk=user.id,
                email=user.email
            )


MIDDLEWARES = (
    (AuthenticationMiddleware, {'backend': JWTAuthenticationBackend()}),
)
