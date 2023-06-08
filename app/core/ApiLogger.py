"""
Created: 02.06.2023
Description:
    * This Module manage logging configuration.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import traceback

from app.util.CommonApiUtil import get_working_dir

import logging


def load_logger_config():
    working_dir = get_working_dir()
    config_path = r'{}app/logging.conf'.format(working_dir)
    try:
        logging.config.fileConfig(config_path)
    except Exception as e:
        print(f'Could not load configuration from path {config_path}')
        traceback.print_exc()