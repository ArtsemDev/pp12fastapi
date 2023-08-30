from pathlib import Path

from dotenv import load_dotenv

from .types import Settings


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS = Settings()
