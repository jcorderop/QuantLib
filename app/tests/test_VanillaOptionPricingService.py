"""
Created: 22.05.2023
Description:
    * The scope of this module is to test.py the VanillaOptionPricingService functionality.
"""
__author__ = "OE - JC"

from app.service.Pricing.Option.OptionRequest import AmericanOptionPriceRequest, EuropeanOptionPriceRequest
from app.service.Pricing.Option.OptionPricingService import OptionPricingService
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.service.Pricing.Option.EnumOptionPricingService import OptionTypeEnum


def test_calculate_american_call_option_price():
    # given
    option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                maturity_date=datetime.now() + relativedelta(years=+1),
                                                spot_price=130.0,
                                                strike_price=130.0,
                                                volatility=0.20,
                                                risk_free_rate=0.001,
                                                dividend_rate=0.015,
                                                option_type=OptionTypeEnum.CALL)
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta > 0.0
    assert price.gamma > 0.0
    assert price.vega == 0.0


def test_calculate_american_put_option_price():
    # given
    option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                maturity_date=datetime.now() + relativedelta(years=+1),
                                                spot_price=130.0,
                                                strike_price=130.0,
                                                volatility=0.20,
                                                risk_free_rate=0.001,
                                                dividend_rate=0.015,
                                                option_type=OptionTypeEnum.PUT)
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma > 0.0
    assert price.vega == 0.0


def test_calculate_european_call_option_price():
    # given
    option_request = EuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                maturity_date=datetime.now() + relativedelta(years=+1),
                                                spot_price=130.0,
                                                strike_price=130.0,
                                                volatility=0.20,
                                                risk_free_rate=0.001,
                                                dividend_rate=0.015,
                                                option_type=OptionTypeEnum.CALL)
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta > 0.0
    assert price.gamma > 0.0
    assert price.vega > 0.0


def test_calculate_european_put_option_price():
    # given
    option_request = EuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                maturity_date=datetime.now() + relativedelta(years=+1),
                                                spot_price=130.0,
                                                strike_price=130.0,
                                                volatility=0.20,
                                                risk_free_rate=0.001,
                                                dividend_rate=0.015,
                                                option_type=OptionTypeEnum.PUT)
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma > 0.0
    assert price.vega > 0.0


def test_calculate_option_price_expired():
    # given
    option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                maturity_date=datetime.now(),
                                                spot_price=127.62,
                                                strike_price=130.0,
                                                volatility=0.20,
                                                risk_free_rate=0.001,
                                                dividend_rate=0.015,
                                                option_type=OptionTypeEnum.PUT)
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price == 0.0
    assert price.delta == 0.0
    assert price.gamma == 0.0
    assert price.vega == 0.0


def test_calculate_option_price_invalid_strike_price():
    # given
    with pytest.raises(ValueError):
        option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                    maturity_date=datetime.now() + relativedelta(years=+1),
                                                    spot_price=None,
                                                    strike_price=127.62,
                                                    volatility=0.20,
                                                    risk_free_rate=0.001,
                                                    dividend_rate=0.015,
                                                    option_type=OptionTypeEnum.PUT)
        pricing_service = OptionPricingService()

    # when
    # then


def test_calculate_option_price_invalid_strike_price():
    # given
    with pytest.raises(ValueError):
        option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                    maturity_date=datetime.now() + relativedelta(years=+1),
                                                    spot_price=127.62,
                                                    strike_price=None,
                                                    volatility=0.20,
                                                    risk_free_rate=0.001,
                                                    dividend_rate=0.015,
                                                    option_type=OptionTypeEnum.PUT)
        pricing_service = OptionPricingService()

    # when
    # then


def test_calculate_option_price_invalid_volatility():
    # given
    with pytest.raises(ValueError):
        option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                    maturity_date=datetime.now() + relativedelta(years=+1),
                                                    spot_price=127.62,
                                                    strike_price=130.0,
                                                    volatility=None,
                                                    risk_free_rate=0.001,
                                                    dividend_rate=0.015,
                                                    option_type=OptionTypeEnum.PUT)
        pricing_service = OptionPricingService()


    # when
    # then


def test_calculate_option_price_invalid_risk_free_rate():
    # given
    with pytest.raises(ValueError):
        option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                    maturity_date=datetime.now() + relativedelta(years=+1),
                                                    spot_price=127.62,
                                                    strike_price=130.0,
                                                    volatility=0.20,
                                                    risk_free_rate=None,
                                                    dividend_rate=0.015,
                                                    option_type=OptionTypeEnum.PUT)
        pricing_service = OptionPricingService()

    # when
    # then


def test_calculate_option_price_invalid_dividend_rate():
    # given
    with pytest.raises(ValueError):
        option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                    maturity_date=datetime.now() + relativedelta(years=+1),
                                                    spot_price=127.62,
                                                    strike_price=130.0,
                                                    volatility=0.20,
                                                    risk_free_rate=0.01,
                                                    dividend_rate=None,
                                                    option_type=OptionTypeEnum.PUT)
        pricing_service = OptionPricingService()

    # when
    # then


def test_calculate_option_price_invalid_option_type():
    # given
    with pytest.raises(ValueError):
        # given
        option_request = AmericanOptionPriceRequest(issue_date=datetime.now(),
                                                    maturity_date=datetime.now() + relativedelta(years=+1),
                                                    spot_price=127.62,
                                                    strike_price=130.0,
                                                    volatility=0.20,
                                                    risk_free_rate=0.001,
                                                    dividend_rate=0.015,
                                                    option_type=None)
        pricing_service = OptionPricingService()

    # when
    # then

