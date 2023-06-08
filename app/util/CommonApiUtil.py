"""
Created: 22.05.2023
Description:
    * This Library offers common functionality used for the application.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import os
import uuid


def get_working_dir():
    return os.path.abspath(__file__).split('app')[0]


def get_index_template_path() -> str:
    working_dir = get_working_dir()
    return r'{}app/static/template/index.template'.format(working_dir)


def get_index_file_path() -> str:
    working_dir = get_working_dir()
    return r'{}app/static/template/index.html'.format(working_dir)


def get_readme_mb_path() -> str:
    working_dir = get_working_dir()
    return r'{}README.md'.format(working_dir)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_id() -> str:
    return str(uuid.uuid4())


def rounding(value: float, dp: int = 6) -> float:
    return round(round(value * 1e9) / 1e9, dp)


