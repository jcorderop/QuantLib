"""
Created: 30.05.2023
Description:
    * This Module defines the enum used for the market data infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from enum import Enum


class MarketDataServiceType(Enum):
    BenchmarkPoints = 'BenchmarkPoints'
    Stock = 'Stock'