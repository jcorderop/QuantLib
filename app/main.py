"""
Created: 22.05.2023
Description:
    * This the entry point and main application that will configure & create the OpenAPI and start the web server.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from app.core.ApiLogger import load_logger_config
from app.core.ApiException import ApiException
from app.controller.Controller import PricingController
from app.core.HomePageBuilder import build_root_web
from app.util.AzureCommonUtil import get_api_settings

logger = logging.getLogger(__name__)
load_logger_config()


def configure_rest_api() -> FastAPI:
    controller = PricingController(get_api_settings())
    controller.set_up()
    return controller.get_app()


def pre_startup() -> FastAPI:
    app = configure_rest_api()
    build_root_web()
    return app


app = pre_startup()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.exception_handler(ApiException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": exc.detail}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Unexpected Exception, contact support"}
    )


if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True, host="0.0.0.0")