"""
Created: 22.05.2023
Description:
    * The scope of this module is to test.py the Rest End-Points.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi.testclient import TestClient
import pytest

from app.controller.routers.OptionPricingRouter import END_POINT_VANILLA_AMERICAN, END_POINT_VANILLA_EUROPEAN
from app.main import configure_rest_api
from app.util.config.OpenApiDocumentation import API_PREFIX
from app.core.ApiClient import get_token

import logging

logger = logging.getLogger(__name__)

TEST_PORT = 9000
app = configure_rest_api()
pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_root():
    # given
    token = await get_token()
    print('Beginning with test.py >>> test_root')
    with TestClient(app) as client:
        # when
        api_response = client.get(
            f'http://localhost:{TEST_PORT}/',
            headers={'Authorization': f'Bearer {token}'},
        )

        # then
        assert api_response.is_success
        assert api_response.status_code == 200


@pytest.mark.asyncio
async def test_fetch_user_auth():
    # given
    token = await get_token()
    print('Beginning with test.py >>> test_fetch_user_auth')
    with TestClient(app) as client:
        # when
        api_response = client.get(
            f'http://localhost:{TEST_PORT}{API_PREFIX}/user/fetch_user_auth',
            headers={'Authorization': f'Bearer {token}'},
        )

        # then
        assert api_response.is_success
        assert api_response.status_code == 200
        assert api_response.json() is not None
        assert api_response.json()['name'] == 'Default'
        assert api_response.json()['preferred_username'] == 'Default'


@pytest.mark.asyncio
async def test_american_vanilla_option_calculation():
    # given
    token = await get_token()
    print('Beginning with test.py >>> test_american_vanilla_option_calculation')
    with TestClient(app) as client:
        # when
        api_response = client.post(
            f'http://localhost:{TEST_PORT}{API_PREFIX}{END_POINT_VANILLA_AMERICAN}',
            headers={'Authorization': f'Bearer {token}'},
            json={
              "issue_date": "2023-05-26",
              "maturity_date": "2024-05-26",
              "spot_price": 150.0,
              "strike_price": 150.0,
              "volatility": 0.20,
              "risk_free_rate": 0.015,
              "dividend_rate": 0.018,
              "option_type": "call"
            },
        )

        # then
        assert api_response.is_success
        assert api_response.status_code == 200
        assert api_response.json() is not None
        assert api_response.json()['option_price'] > 0


@pytest.mark.asyncio
async def test_european_vanilla_option_calculation():
    # given
    token = await get_token()
    print('Beginning with test.py >>> test_european_vanilla_option_calculation')
    with TestClient(app) as client:
        # when
        api_response = client.post(
            f'http://localhost:{TEST_PORT}{API_PREFIX}{END_POINT_VANILLA_EUROPEAN}',
            headers={'Authorization': f'Bearer {token}'},
            json={
              "issue_date": "2023-05-26",
              "maturity_date": "2024-05-26",
              "spot_price": 150.0,
              "strike_price": 150.0,
              "volatility": 0.20,
              "risk_free_rate": 0.015,
              "dividend_rate": 0.018,
              "option_type": "call"
            },
        )

        # then
        assert api_response.is_success
        assert api_response.status_code == 200
        assert api_response.json() is not None
        assert api_response.json()['option_price'] > 0