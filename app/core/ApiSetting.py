"""
Created: 22.05.2023
Description:
    * This Module offers common functionality to load the configuration required for the application
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from typing import Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, Field

load_dotenv()


class ApiSettings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[Union[str, AnyHttpUrl]] = ['http://localhost:8000']
    OPENAPI_CLIENT_ID: str = Field(default='', env='OPENAPI_CLIENT_ID')
    SERVER_API_ID: str = Field(default='', env='SERVER_API_ID')
    TENANT_ID: str = Field(default='', env='TENANT_ID')
    API_HOST: str = Field(default='', env='API_HOST')
    API_PORT: str = Field(default='', env='API_PORT')

    class Config:
        env_file = '../../.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

