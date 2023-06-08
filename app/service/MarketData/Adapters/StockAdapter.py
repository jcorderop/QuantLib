"""
Created: 30.05.2023
Description:
    * This Module is an adapter to fetch stock prices and calculate some market data.
    * The initial version gets data from https://finance.yahoo.com/
"""
__author__ = "OE - JC"

from pandas import DataFrame

from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import numpy as np

from app.service.MarketData.BaseMarketDataService import MarketDataAdapter, StockResponse

import logging

from app.util.CommonApiUtil import rounding

logger = logging.getLogger(__name__)


class StockAdapter(MarketDataAdapter):

    def __init__(self):
        self.repository = StockRepository()

    def execute(self, id: str) -> StockResponse:
        logger.info(f'Fetching Stock Market Data from ticker [{id}]...')
        return self.query_stock_data(id)

    def query_stock_data(self, id: str) -> StockResponse:
        stock_data = self.find_by_id(id)
        if stock_data is None:
            stock_data = StocksConnector.fetch_stock_data(id)
            self.save(id, stock_data)
        return stock_data

    def find_by_id(self, id: str) -> StockResponse:
        return self.repository.find_by_id(id)

    def save(self, id: str, benchmark_points: StockResponse):
        self.repository.save(id, benchmark_points)


class StockRepository:

    __CACHE = {}  # TODO it can be changed to a Database later

    def find_by_id(self, id: str) -> StockResponse:
        stock_data = self.__CACHE.get(id, None)
        if stock_data and stock_data.last_update < datetime.now().date():
            logger.info('Data from [{id}] is old and has to be refreshed..')
            stock_data = None
            self.save(id, stock_data)
        return stock_data

    def save(self, id: str, stock_data: StockResponse):
        self.__CACHE[id] = stock_data


class StocksConnector:
    __WORKING_DAYS = 252
    __HISTORICAL_DATA_PERIOD_IN_YEARS = -1
    __DATE_FORMAT = '%Y-%m-%d'
    __ROUNDING = 3

    @staticmethod
    def fetch_stock_data(id: str) -> StockResponse:
        stock_data = StocksConnector.get_tick(id)
        stock_data = StocksConnector.add_volatility(id, stock_data)
        return stock_data

    @staticmethod
    def get_tick(ticker: str) -> StockResponse:
        logger.info(f'Fetching Stock Market Data from source www.yahoo.finance.com, ticker [{id}]...')
        stock = yf.Ticker(ticker)
        historical_data = stock.history(period="1d")

        last_price = historical_data["Close"].iloc[-1]
        close_price = historical_data["Close"].iloc[-1]
        high_price = historical_data["High"].iloc[-1]
        low_price = historical_data["Low"].iloc[-1]
        open_price = historical_data["Open"].iloc[-1]
        volume = historical_data["Volume"].iloc[-1]

        return StockResponse(ticker=ticker,
                             last=rounding(last_price, dp=StocksConnector.__ROUNDING),
                             close=rounding(close_price, dp=StocksConnector.__ROUNDING),
                             high=rounding(high_price, dp=StocksConnector.__ROUNDING),
                             low=rounding(low_price, dp=StocksConnector.__ROUNDING),
                             open=rounding(open_price, dp=StocksConnector.__ROUNDING),
                             volume=rounding(volume, dp=StocksConnector.__ROUNDING),
                             last_update=datetime.now().date())

    @staticmethod
    def add_volatility(ticker: str, stock_data: StockResponse) -> StockResponse:
        logger.info(f'Calculating constant volatility, ticker [{id}]...')
        volatility = StocksConnector.calculate_volatility(ticker)
        return StockResponse(ticker=stock_data.ticker,
                             last=stock_data.last,
                             close=stock_data.close,
                             high=stock_data.high,
                             low=stock_data.low,
                             open=stock_data.open,
                             volume=stock_data.volume,
                             volatility=rounding(volatility, dp=StocksConnector.__ROUNDING),
                             last_update=datetime.now().date())

    @staticmethod
    def calculate_volatility(ticker: str) -> float:
        start_date = (datetime.now().date() + relativedelta(years=StocksConnector.__HISTORICAL_DATA_PERIOD_IN_YEARS)).strftime(StocksConnector.__DATE_FORMAT)
        end_date = datetime.now().date().strftime(StocksConnector.__DATE_FORMAT)
        data = StocksConnector.get_historical_data(ticker, start_date, end_date)
        return StocksConnector.calculate_constant_volatility(data)

    @staticmethod
    def get_historical_data(ticker: str, start_date: str, end_date: str) -> DataFrame:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date, end=end_date)
        return historical_data

    @staticmethod
    def calculate_constant_volatility(historical_data: DataFrame) -> float:
        log_returns = np.log(historical_data["Close"] / historical_data["Close"].shift(1))
        return log_returns.std() * np.sqrt(StocksConnector.__WORKING_DAYS)