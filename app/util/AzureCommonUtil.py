"""
Created: 22.05.2023
Description:
    * This Library offers common functionality used to interact with Azure.
        e.g.: Azure Active Directory
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from app.core.ApiSetting import ApiSettings

__API_SETTINGS = None


def get_api_settings() -> ApiSettings:
    global __API_SETTINGS
    if __API_SETTINGS is None:
        __API_SETTINGS = ApiSettings()
    return __API_SETTINGS


def get_azure_scheme() -> SingleTenantAzureAuthorizationCodeBearer:
    settings = get_api_settings()
    return SingleTenantAzureAuthorizationCodeBearer(
        app_client_id=settings.SERVER_API_ID,
        tenant_id=settings.TENANT_ID,
        allow_guest_users=True,
        scopes={
            f'api://{settings.SERVER_API_ID}/user_impersonation': 'user_impersonation',
        }
    )