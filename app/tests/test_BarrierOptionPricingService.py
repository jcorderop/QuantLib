"""
Created: 22.05.2023
Description:
    * The scope of this module is to test.py the VanillaOptionPricingService functionality.
"""
__author__ = "OE - JC"

from app.service.Pricing.Option.OptionRequest import AmericanOptionPriceRequest, EuropeanOptionPriceRequest, \
    BarrierEuropeanOptionPriceRequest, BarrierOption
from app.service.Pricing.Option.OptionPricingService import OptionPricingService
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.service.Pricing.Option.EnumOptionPricingService import OptionTypeEnum, BarrierTypeEnum


def test_calculate_up_and_in_european_call_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.CALL,
                                                       barrier=BarrierOption(barrier_price=140.0,
                                                                             barrier_type=BarrierTypeEnum.UP_AND_IN)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta > 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0


def test_calculate_up_and_out_european_call_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.CALL,
                                                       barrier=BarrierOption(barrier_price=140.0,
                                                                             barrier_type=BarrierTypeEnum.UP_AND_IN)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta > 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0



def test_calculate_down_and_in_european_call_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.CALL,
                                                       barrier=BarrierOption(barrier_price=120.0,
                                                                             barrier_type=BarrierTypeEnum.DOWN_AND_IN)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0


def test_calculate_down_and_out_european_call_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.CALL,
                                                       barrier=BarrierOption(barrier_price=120.0,
                                                                             barrier_type=BarrierTypeEnum.DOWN_AND_OUT)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta > 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0


def test_calculate_up_and_out_european_call_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.CALL,
                                                       barrier=BarrierOption(barrier_price=140.0,
                                                                             barrier_type=BarrierTypeEnum.UP_AND_OUT)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma < 0.0
    # assert price.vega > 0.0



def test_calculate_up_and_in_european_put_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.PUT,
                                                       barrier=BarrierOption(barrier_price=140.0,
                                                                             barrier_type=BarrierTypeEnum.UP_AND_IN)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta > 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0


def test_calculate_up_and_out_european_put_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.PUT,
                                                       barrier=BarrierOption(barrier_price=140.0,
                                                                             barrier_type=BarrierTypeEnum.UP_AND_OUT)
    )
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0


def test_calculate_down_and_in_european_put_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.PUT,
                                                       barrier=BarrierOption(barrier_price=100.0,
                                                                             barrier_type=BarrierTypeEnum.DOWN_AND_IN))
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma > 0.0
    # assert price.vega > 0.0


def test_calculate_down_and_out_european_put_option_price():
    # given
    option_request = BarrierEuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                       maturity_date=datetime.now() + relativedelta(years=+1),
                                                       spot_price=130.0,
                                                       strike_price=130.0,
                                                       volatility=0.20,
                                                       risk_free_rate=0.001,
                                                       dividend_rate=0.015,
                                                       option_type=OptionTypeEnum.PUT,
                                                       barrier=BarrierOption(barrier_price=100.0,
                                                                             barrier_type=BarrierTypeEnum.DOWN_AND_OUT))
    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)

    # then
    assert price is not None
    assert price.option_price > 0.0
    assert price.delta < 0.0
    assert price.gamma < 0.0
    # assert price.vega > 0.0

