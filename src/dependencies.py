from fastapi import Depends
from sqlalchemy.orm import Session

from .database.models import Base


def _get_db_session() -> Session:
    session = Base.session()
    try:
        yield session
    finally:
        session.close()


get_db_session = Depends(_get_db_session)
