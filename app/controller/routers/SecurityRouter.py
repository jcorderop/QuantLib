"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for security loading at start-up of the server.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import APIRouter
from app.util.AzureCommonUtil import get_azure_scheme

import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await get_azure_scheme().openid_config.load_config()