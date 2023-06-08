"""
Created: 05.06.2023
Description:
    * This Module offer common functionality for yield curve construction
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql
from httpx import AsyncClient, HTTPError

from app.core.ApiSetting import ApiSettings
from app.controller.routers.MarketDataRouter import END_POINT_BENCHMARK_POINTS
from app.core.ApiClient import get_token
from app.core.ApiException import ApiException
from app.service.Pricing.Option.EnumOptionPricingService import CountryInterestRateId
from app.util.config.OpenApiDocumentation import API_PREFIX

import logging

logger = logging.getLogger(__name__)


async def fetch_benchmark_points(country: CountryInterestRateId,
                                 app_settings: ApiSettings) -> dict:
    logger.info('Fetching benchmark points...')
    try:
        token = await get_token()
        response = await AsyncClient().get(
            url=f'http://{app_settings.API_HOST}:{app_settings.API_PORT}{API_PREFIX}{END_POINT_BENCHMARK_POINTS}{country.value}',
            headers={'Authorization': f'Bearer {token}'},
            timeout=20)
        response.raise_for_status()
        logger.info('Finished to fetch benchmark points...')
        return response.json()
    except HTTPError as e:
        raise ApiException('Could not fetch benchmark points...')


def get_tenor(tenor: str) -> ql.Period:
    tenor_split = tenor.split(' ')
    period = None
    tenor_value = int(tenor_split[0])
    if tenor_split[1] == 'day':
        period = ql.Period(tenor_value, ql.Days)
    elif tenor_split[1] == 'week':
        period = ql.Period(tenor_value, ql.Months)
    elif tenor_split[1] == 'month':
        period = ql.Period(tenor_value, ql.Months)
    elif tenor_split[1] == 'year':
        period = ql.Period(tenor_value, ql.Years)
    else:
        logger.error('Invalid Tenor, benchmark points cannot be processed.')
    return period