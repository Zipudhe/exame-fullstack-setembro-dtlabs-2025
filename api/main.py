from contextlib import asynccontextmanager
import uvicorn
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from config.env_vars import get_allowed_hosts
from config.logging import setup_logger

from src.devices.router import router as devicesRouter
from src.users.router import router as usersRouter
from src.database import check_client_connection

setup_logger()


logger = logging.getLogger(__name__)

allowed_hosts = get_allowed_hosts()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application custom startup")
    check_client_connection()
    yield


app = FastAPI(
    title="dt-labs IoT",
    description="API to manage and monitoring IoT devices",
    version="1.0.0",
    lifespan=lifespan,
)

CORSMiddleware(app, allow_origins=allowed_hosts)

app.include_router(usersRouter, prefix="/api", tags=["Users"])
app.include_router(devicesRouter, prefix="/api", tags=["Devices"])


@app.get("/")
def default():
    return {"Hello": "World"}


if __name__ == "__main__":
    from config.env_vars import get_port, get_enviroment

    port = get_port()
    env = get_enviroment()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        reload=True if env == "development" else False,
    )
