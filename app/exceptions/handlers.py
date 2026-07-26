from typing import Any, Callable

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import logger
from app.exceptions.base import InventoryException

async def validation_exception_handler(request: Request, exception: RequestValidationError):
    body = await request.body()
    logger.debug("Validation error occured")
    logger.debug(f"Request body: {body.decode()}")
    logger.debug(f"Validation errors: {exception.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Request validation failed",
            "detail": jsonable_encoder(exception.errors())
        }
    )

def create_exception_handler(status_code: int, message: str) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exception: InventoryException) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "message": message
            }
        )

    return exception_handler