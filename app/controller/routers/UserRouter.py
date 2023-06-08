"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for user relevant data End-Point.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import Depends, Request, APIRouter

from app.util.config.OpenApiDocumentation import Tags
from app.util.AzureCommonUtil import get_azure_scheme
from app.core.model.UserAuth import UserAuth, build_user_auth

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


END_POINT_FETCH_USER = "/user/fetch_user_auth"


@router.get(
    END_POINT_FETCH_USER,
    response_model=UserAuth,
    dependencies=[Depends(get_azure_scheme())],
    tags=[Tags.user],
    summary="Who am I?",
    description="This End-point is used to fetch user logged-in.",
    response_description="User name.",
)
async def fetch_user_auth(request: Request) -> UserAuth:
    return build_user_auth(request)

