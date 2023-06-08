"""
Created: 22.05.2023
Description:
    * This Module is used to handle the creation of the OpenAPI application.
    * To add the roting of the application.
    * To configure and require the authentication on swagger.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller.routers import SecurityRouter, RootRouter, UserRouter, OptionPricingRouter, MarketDataRouter, \
    YieldCurveRouter, FixedIncomePricingRouter
from app.core.ApiSetting import ApiSettings
from app.util.config.OpenApiDocumentation import *
from starlette.staticfiles import StaticFiles

import logging

from app.util.CommonApiUtil import get_working_dir

logger = logging.getLogger(__name__)


class PricingController:

    def __init__(self, settings: ApiSettings):
        self.__settings = settings
        self.__app = None

    def set_up(self) -> None:
        self.__app = self._create_fast_api()
        self._configure_cors_origin()
        self._add_routers()
        self._mount()

    def _add_routers(self) -> None:
        self.__app.include_router(SecurityRouter.router)
        self.__app.include_router(RootRouter.router, include_in_schema=False)
        self.__app.include_router(UserRouter.router, prefix=API_PREFIX)
        self.__app.include_router(MarketDataRouter.router, prefix=API_PREFIX)
        self.__app.include_router(YieldCurveRouter.router, prefix=API_PREFIX)
        self.__app.include_router(OptionPricingRouter.router, prefix=API_PREFIX)
        self.__app.include_router(FixedIncomePricingRouter.router, prefix=API_PREFIX)

    def _mount(self) -> None:
        working_dir = get_working_dir()
        self.__app.mount('/app/static', StaticFiles(directory=r'{}app/static'.format(working_dir), html=True), name='static')

    def _create_fast_api(self) -> FastAPI:
        app = FastAPI(
            swagger_ui_oauth2_redirect_url='/oauth2-redirect',
            swagger_ui_init_oauth={
                'usePkceWithAuthorizationCodeGrant': True,
                'clientId': self.__settings.OPENAPI_CLIENT_ID,
            },
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            terms_of_service=TERMS_OF_SERVICES,
            contact=CONTACT,
            license_info=LICENSE_INFO,
        )
        return app

    def _configure_cors_origin(self):
        if self.__settings.BACKEND_CORS_ORIGINS:
            self.__app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.__settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*'],
            )

    def get_app(self) -> FastAPI:
        return self.__app