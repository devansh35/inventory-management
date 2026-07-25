import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.config import APP_HOST, APP_PORT, logger, debug_mode
from app.core.database import engine
from app.exceptions.handlers import validation_exception_handler
from app.utils.health import check_db_connection
from app.routes import health_routes, product_routes, customer_routes, order_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    
    try:
        if await check_db_connection():
            logger.info("Database connection successful")
        else:
            raise RuntimeError("Database connection failed")
    except Exception as e:
        logger.error(f"Error checking database connection: {e}")
        raise

    yield
    
    logger.info("Shutting down...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan, debug=debug_mode)

app.include_router(health_routes.router)
app.include_router(product_routes.router)
app.include_router(customer_routes.router)
app.include_router(order_routes.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)