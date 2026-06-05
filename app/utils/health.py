from sqlalchemy import text

from app.core.database import SessionLocal
from app.config import logger

async def check_db_connection():
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False