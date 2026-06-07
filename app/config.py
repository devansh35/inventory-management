import os
import logging

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5433))
DB_NAME = os.getenv("DB_NAME", "inventory_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

ALEMBIC_DATABASE_URL = (
    f"postgresql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

logger = logging.getLogger()

debug_mode = os.getenv("DEBUG", "False").lower() in (
    "true", "1", "yes", "y", "t"
)

if debug_mode:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.getLogger("uvicorn.access").disabled = True