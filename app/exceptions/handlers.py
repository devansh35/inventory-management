from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import logger

async def validation_exception_handler(request: Request, exception: RequestValidationError):
    body = await request.body()
    logger.debug("Validation error occured")
    logger.debug(f"Request body: {body.decode()}")
    logger.debug(f"Validation errors: {exception.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": jsonable_encoder(exception.errors()),
            "message": "Request validation failed"
        }
    )