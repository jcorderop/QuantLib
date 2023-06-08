"""
Created: 22.05.2023
Description:
    * This Model is used to store the relevant data of the user authenticated.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from typing import Optional
from fastapi import Request
from pydantic import BaseModel


class UserAuth(BaseModel):
    name: str
    preferred_username: Optional[str]


def build_user_auth(request: Request) -> UserAuth:
    name = request.state.user.dict().get('name', 'Default')
    if name is None:
        name = 'Default'

    preferred_username = request.state.user.dict().get('preferred_username', 'Default')
    if preferred_username is None:
        preferred_username = 'Default'

    return UserAuth(name=name,
                    preferred_username=preferred_username)