"""
Created: 30.05.2023
Description:
    * This Module defines the classes used for the market data infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from datetime import date
from typing import Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, StrictStr, StrictFloat

from app.core.model.BaseModel import BaseObject

import logging

logger = logging.getLogger(__name__)


class BenchmarkPoint(BaseModel):
    tenor: str
    rate: StrictFloat


class CountryRate(BaseModel):
    country: str
    rate: StrictFloat


class MarketDataResponse(BaseObject):
    pass


class StockResponse(MarketDataResponse):
    ticker: StrictStr
    last: StrictFloat
    close: StrictFloat
    high: StrictFloat
    low: StrictFloat
    open: StrictFloat
    volume: StrictFloat
    volatility: Optional[StrictFloat]
    last_update: date


class BenchmarkPointsResponse(MarketDataResponse):
    benchmark_points: list[BenchmarkPoint]
    last_update: date


class CountryRatesResponse(MarketDataResponse):
    country_rates: list[CountryRate]
    last_update: date


class MarketDataAdapter(ABC):

    @abstractmethod
    def execute(self, id: str) -> MarketDataResponse:
        ...