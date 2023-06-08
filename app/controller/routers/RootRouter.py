"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for the root End-Point.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from mimetypes import guess_type
from typing import AnyStr
from fastapi import APIRouter, Response
from starlette.responses import HTMLResponse
from os.path import isfile

from app.util.CommonApiUtil import get_index_file_path

import logging


logger = logging.getLogger(__name__)

router = APIRouter()


def get_content(filename) -> AnyStr:
    with open(filename) as f:
        content = f.read()
    return content


@router.get("/", response_class=HTMLResponse)
async def root():
    filename = get_index_file_path()
    if not isfile(filename):
        return Response(status_code=404)
    content_type, _ = guess_type(filename)
    return Response(get_content(filename), media_type=content_type)
