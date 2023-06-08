"""
Created: 01.06.2023
Description:
    * This Module contain base model classes
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from pydantic import BaseModel, StrictStr

from app.util.CommonApiUtil import get_id


class BaseObject(BaseModel):
    id: StrictStr = get_id()