from pathlib import Path

from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from passlib.context import CryptContext

from .types import Settings


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS = Settings()
pwd_context = CryptContext(schemes=['bcrypt'])
templating = Jinja2Templates(directory='templates')
