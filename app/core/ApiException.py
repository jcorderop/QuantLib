"""
Created: 01.06.2023
Description:
    * This Module defines the api exceptions
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules


class ApiException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.detail = message