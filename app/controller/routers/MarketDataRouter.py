"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for the market data End-Points.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import Security, APIRouter

from app.util.config.OpenApiDocumentation import Tags
from app.service.MarketData.Adapters.BenchmarkPointsAdapter import BenchmarkPointsResponse
from app.service.MarketData.Adapters.StockAdapter import StockResponse
from app.service.MarketData.EnumMarketDataService import MarketDataServiceType
from app.service.MarketData.MarketDataService import MarketDataService
from app.util.AzureCommonUtil import get_azure_scheme
from app.service.Pricing.Option.EnumOptionPricingService import CountryInterestRateId

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

END_POINT_BENCHMARK_POINTS = "/marketdata/yieldcurve/benchmark/country/"
END_POINT_STOCKS_DATA = "/marketdata/stock/"

@router.get(
    END_POINT_BENCHMARK_POINTS + "{name}",
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.market_data],
    summary="Returns the yield curve benchmark points",
    response_description="Benchmark Points",
    )
async def fetch_benchmark_points(name: CountryInterestRateId) -> BenchmarkPointsResponse:
    """
    This End-Point returns the list of interest rate that can be used as benchmark to calculate yield curve.
    * Use country name, e.g.: switzerland
    """
    logger.info('Benchmark Points Request: {}'.format(name))
    service = MarketDataService(MarketDataServiceType.BenchmarkPoints)
    response = service.fetch_data(name.value)
    logger.info('Benchmark Points Response: {}'.format(response))
    return response


@router.get(
    END_POINT_STOCKS_DATA + "{ticker}",
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.market_data],
    summary="Returns stock market price, volatility",
    response_description="Stock Market Data",
    )
async def fetch_stock_data(ticker: str) -> StockResponse:
    """
    This End-Point returns the stocks market data.

    Data is fetched from yahoo finance at the moment and data is not normilized, follow the ticker convention from this source.
    * Use symbol with ticker, e.g.: ABBN.SW
    """
    logger.info('Benchmark Points Request: {}'.format(ticker))
    service = MarketDataService(MarketDataServiceType.Stock)
    response = service.fetch_data(ticker.upper())
    logger.info('Benchmark Points Response: {}'.format(response))
    return response
