"""
Created: 22.05.2023
Description:
    * Client Library used to handle the token form Azure Active Directory
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import asyncio
import threading
from dotenv import load_dotenv
from httpx import AsyncClient
from pydantic import Field, BaseSettings

from app.core.ApiException import ApiException
from app.util.CommonApiUtil import Singleton

import logging


logger = logging.getLogger(__name__)

load_dotenv()


class Settings(BaseSettings):
    TENANT_ID: str = Field(default='', env='TENANT_ID')
    SERVER_API_ID: str = Field(default='', env='SERVER_API_ID')
    CLIENT_ID: str = Field(default='', env='CLIENT_ID')
    CLIENT_SECRET: str = Field(default='', env='CLIENT_SECRET')

    class Config:
        env_file = '../../.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()


async def request_security_token() -> str:
    async with AsyncClient() as client:
        azure_response = await client.post(
            url=f'https://login.microsoftonline.com/{settings.TENANT_ID}/oauth2/v2.0/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': settings.CLIENT_ID,  # the ID of the app reg you created the secret for
                'client_secret': settings.CLIENT_SECRET,  # the secret you created
                'scope': f'api://{settings.SERVER_API_ID}/.default',  # note: NOT .user_impersonation
            }
        )
        logger.info('Requesting token... {}'.format(azure_response))
        response = azure_response.json()
        return response.get('access_token', None)


class CacheToken(metaclass=Singleton):

    __TOKEN = None
    __lock = threading.Lock()

    def __init__(self):
        self.lock = None

    @classmethod
    def __store_token(cls, new_token) -> None:
        cls.__TOKEN = new_token
        logger.info('Token stored: {}'.format(new_token))

    @classmethod
    async def __request_token(cls) -> str:
        logger.info('Requesting API token...')
        tasks = asyncio.create_task(request_security_token())
        await tasks
        if tasks:
            return tasks.result()
        else:
            raise ApiException('Could not acquire API token...')

    @classmethod
    async def __handler(cls) -> None:
        logger.info("Waiting for the lock to store Token...")
        cls.__lock.acquire()
        try:
            logger.info('API Token has to be requested...')
            token = await cls.__request_token()
            cls.__store_token(token)
        finally:
            logger.info('Lock released...')
            cls.__lock.release()

    @classmethod
    async def get_token(cls) -> str:
        if cls.__TOKEN is None:
            await cls.__handler()
        return cls.__TOKEN


async def get_token():
    token_task = asyncio.create_task(CacheToken.get_token())
    await token_task
    token = token_task.result()
    logger.info('Will Use Token: {}'.format(token))
    return token