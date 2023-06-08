"""
Created: 30.05.2023
Description:
    * This Module is an adapter to fetch government bonds interest rate.
    * The initial version gets data from http://www.worldgovernmentbonds.com/country/
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from datetime import datetime
from jsonpath_ng import parse
from typing import Any
from requests import Response # TODO, remove this dependency
import requests
import html_to_json

from app.core.ApiException import ApiException
from app.service.Pricing.Option.EnumOptionPricingService import CountryInterestRateId
from app.util.CommonApiUtil import rounding
from app.service.MarketData.BaseMarketDataService import MarketDataAdapter, BenchmarkPoint, BenchmarkPointsResponse, \
    CountryRate, CountryRatesResponse

import logging

logger = logging.getLogger(__name__)


class BenchmarkPointsAdapter(MarketDataAdapter):

    def __init__(self):
        self.repository_benchmark = BenchmarkPointsRepository()
        self.repository_country = CountryRateRepository()

    def execute(self, id: str) -> BenchmarkPointsResponse:
        return self.query_interest_rate(id)

    def query_interest_rate(self, id: str) -> BenchmarkPointsResponse:
        if id is CountryInterestRateId.__members__:
            raise ValueError(f'Interest rate id [{id}] not supported.') # TODO check why error is not propagated to swagger
        benchmark_points = self.find_benchmark_by_id(id)
        if benchmark_points is None:
            benchmark_points = InterestRateConnector.fetch_interest_rates(id)
            country_rates = InterestRateConnector.fetch_country_on_rates()
            self.save(id, benchmark_points, country_rates)
            on_rate = self.get_on_rate(id)
            benchmark_points.benchmark_points = [on_rate] + benchmark_points.benchmark_points
        return benchmark_points

    def get_on_rate(self, id: str):
        rate = self.find_country_by_id(id)
        if rate:
            on_rate = BenchmarkPoint(tenor='0 day', rate=rate)
            return on_rate
        else:
            raise Exception(f'ON Rate from country {id} could not be found...')

    def find_benchmark_by_id(self, id: str) -> BenchmarkPointsResponse:
        return self.repository_benchmark.find_by_id(id)

    def find_country_by_id(self, id: str) -> float:
        return self.repository_country.find_by_id(id)

    def save(self,
             id: str,
             benchmark_points: BenchmarkPointsResponse,
             country_rates: CountryRatesResponse):
        self.repository_benchmark.save(id, benchmark_points)
        self.repository_country.save(country_rates)


class BenchmarkPointsRepository:

    __CACHE = {} # TODO it can be changed to a Database later

    def find_by_id(self, id: str) -> BenchmarkPointsResponse:
        benchmark_points = self.__CACHE.get(id, None)
        if benchmark_points and benchmark_points.last_update < datetime.now().date():
            logger.info('Data from [{id}] is old and has to be refreshed..')
            benchmark_points = None
            self.save(id, benchmark_points)
        return benchmark_points

    def save(self, id: str, benchmark_points: BenchmarkPointsResponse):
        self.__CACHE[id] = benchmark_points


class CountryRateRepository:
    __CACHE = {}  # TODO it can be changed to a Database later

    def find_by_id(self, id: str) -> float:
        return self.__CACHE[id.upper()]

    def save(self, country_rates: CountryRatesResponse):
        for on in country_rates.country_rates:
            self.__CACHE[on.country.upper()] = on.rate


class InterestRateConnectorSettings:
    URL_COUNTRY = 'http://www.worldgovernmentbonds.com/country/{}'
    URL_BANK_RATES = 'http://www.worldgovernmentbonds.com/central-bank-rates/'


class InterestRateConnector:
    @staticmethod
    def find_content(output_json, node_target):
        result = None
        if output_json and len(output_json) > 0:
            if isinstance(output_json, list):
                expression = parse(f'$.{node_target}')
                for next_node in output_json:
                    table_matches = [match.value for match in expression.find(next_node)]
                    if table_matches:
                        return table_matches
                    result = InterestRateConnector.find_content(next_node, node_target)
                    if result:
                        return result
            if isinstance(output_json, dict):
                for node_name in output_json:
                    result = InterestRateConnector.find_content(output_json[node_name], node_target)
                    if result:
                        return result
        return result

    @staticmethod
    def get_content(output_json, target_node_name):
        content = InterestRateConnector.find_content(output_json, target_node_name)
        if content:
            logger.info(f'Target content: [{target_node_name}] found')
        else:
            raise ApiException(f'Loading interest rates, target content: [{target_node_name}] not found')
        return content

    @staticmethod
    def convert_html_to_json(response: Response) -> dict:
        return html_to_json.convert(response.text)

    @staticmethod
    def get_table_content(html_as_json: dict) -> list[Any]:
        return InterestRateConnector.get_content(html_as_json, 'table')

    @staticmethod
    def convert_interest_rate(interest_rate: str) -> float:
        return rounding(float(interest_rate.replace('%', '')) / 100)

    @staticmethod
    def get_interest_rate(node_row) -> float:
        expression_rate = parse("$.[*][*].b[*]._value")
        matches_rate = [match.value for match in expression_rate.find(node_row)]
        return InterestRateConnector.convert_interest_rate(matches_rate[0])

    @staticmethod
    def convert_tenor_to_date(tenor: str) -> str:
        tenor_split = tenor.split(' ')
        if 'day' in tenor_split[1]:
            return  f'{tenor_split[0]} day'
        elif 'month' in tenor_split[1]:
            return  f'{tenor_split[0]} month'
        elif 'year' in tenor_split[1]:
            return f'{tenor_split[0]} year'
        else:
            logger.error('Could not process tenor: [{tenor}]')

    @staticmethod
    def get_tenor(node_row: list) -> str:
        expression_tenor = parse("$.[*][*].a[*].b[*]._value")
        matches_tenor = [match.value for match in expression_tenor.find(node_row)]
        return InterestRateConnector.convert_tenor_to_date(matches_tenor[0])

    @staticmethod
    def get_country(node_row: list) -> str:
        expression_tenor = parse("$.[*].b[*].a[*]._value")
        matches_tenor = [match.value for match in expression_tenor.find(node_row)]
        return matches_tenor[0]

    @staticmethod
    def get_country_rate(node_row: list) -> float:
        expression_tenor = parse("$.[*].b[*]._value")
        matches_tenor = [match.value for match in expression_tenor.find(node_row)]
        return InterestRateConnector.convert_interest_rate(matches_tenor[0])

    @staticmethod
    def get_body_rows(content: list) -> Any:
        expression_row = parse("$.[*][*].tr[*][*].td")
        matches_rows = [match.value for match in expression_row.find(content)]
        return matches_rows

    @staticmethod
    def get_benchmark_points(html_as_json: list) -> list:
        benchmark_points = []
        content = InterestRateConnector.get_content(html_as_json, 'tbody')
        matches_rows = InterestRateConnector.get_body_rows(content)
        for node_row in matches_rows:
            tenor = InterestRateConnector.get_tenor(node_row)
            rate = InterestRateConnector.get_interest_rate(node_row)
            benchmark_points.append(BenchmarkPoint(tenor=tenor, rate=rate))
        return benchmark_points

    @staticmethod
    def get_country_on_rates(html_as_json: list) -> list:
        country_rates = []
        content = InterestRateConnector.get_content(html_as_json, 'tbody')
        matches_rows = InterestRateConnector.get_body_rows(content)
        for node_row in matches_rows:
            try:
                country = InterestRateConnector.get_country(node_row)
                rate = InterestRateConnector.get_country_rate(node_row)
                country_rates.append(CountryRate(country=country, rate=rate))
            except Exception as e:
                logger.error(f'Could not process row: reason {e}')
        return country_rates

    @staticmethod
    def fetch_interest_rates(id: str) -> BenchmarkPointsResponse:
        url = InterestRateConnectorSettings.URL_COUNTRY.format(id)
        logger.info(f'Loading data from {url} ...')
        response = requests.get(url)

        if response.status_code == 200:
            logger.info('Response successfully, building benchmark points...')
            output_json = InterestRateConnector.convert_html_to_json(response)
            table_content = InterestRateConnector.get_table_content(output_json)
            benchmark_points = InterestRateConnector.get_benchmark_points(table_content)
            logger.info('Benchmark points, created...')
            return BenchmarkPointsResponse(benchmark_points=benchmark_points,
                                           last_update=datetime.now().date())
        else:
            raise ApiException(f'Could not fetch interest rates from: {url}, status code: {response.status_code}')

    @staticmethod
    def fetch_country_on_rates() -> CountryRatesResponse:
        url = InterestRateConnectorSettings.URL_BANK_RATES
        logger.info(f'Loading data from {url} ...')
        response = requests.get(url)

        if response.status_code == 200:
            logger.info('Response successfully, building Country Rates...')
            output_json = InterestRateConnector.convert_html_to_json(response)
            table_content = InterestRateConnector.get_table_content(output_json)
            country_rate = InterestRateConnector.get_country_on_rates(table_content)
            logger.info('Country Rates, created...')
            return CountryRatesResponse(country_rates=country_rate,
                                        last_update=datetime.now().date())
        else:
            raise ApiException(f'Could not fetch Country Rates from: {url}, status code: {response.status_code}')

