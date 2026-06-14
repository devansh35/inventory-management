from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.config import logger
from app.utils.health import check_db_connection

router = APIRouter()

@router.get("/health")
async def health_check():
    if await check_db_connection():
        return {"status": "UP"}
    else:
        logger.error("Health check failed")
        return JSONResponse(status_code=503, content={"status": "DOWN"})