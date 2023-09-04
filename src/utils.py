from datetime import datetime, timedelta

from jose import jwt, JWTError

from .settings import pwd_context, SETTINGS


def create_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(secret=password, hash=hash_password)


def create_access_token(sub: str) -> str:
    return jwt.encode(
        claims={
            'sub': sub,
            'exp': datetime.utcnow() + timedelta(minutes=SETTINGS.ACCESS_EXP_TOKEN)
        },
        key=SETTINGS.SECRET_STR.get_secret_value(),
        algorithm=SETTINGS.ALGORITHM
    )


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token=token,
            key=SETTINGS.SECRET_STR.get_secret_value(),
            algorithms=SETTINGS.ALGORITHM
        )
    except JWTError:
        return {}
    else:
        return payload
