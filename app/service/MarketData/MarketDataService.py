"""
Created: 30.05.2023
Description:
    * This Service is designed to provide market data.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from app.service.MarketData.Adapters.BenchmarkPointsAdapter import BenchmarkPointsAdapter
from app.service.MarketData.Adapters.StockAdapter import StockAdapter
from app.service.MarketData.BaseMarketDataService import MarketDataResponse
from app.service.MarketData.EnumMarketDataService import MarketDataServiceType

import logging

logger = logging.getLogger(__name__)


class MarketDataServiceFactory:
    instance = {
        MarketDataServiceType.Stock: StockAdapter,
        MarketDataServiceType.BenchmarkPoints: BenchmarkPointsAdapter
    }


class MarketDataService:

    def __init__(self, service: MarketDataServiceType):
        self.service = service
        self.adapter = MarketDataServiceFactory.instance[service]()

    def fetch_data(self, id: str) -> MarketDataResponse:
        return self.adapter.execute(id)
