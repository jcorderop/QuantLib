"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for the pricing End-Points.
"""
__author__ = "OE - JC"

from app.service.Pricing.Option.OptionRequest import BarrierEuropeanOptionPriceRequest
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import Security, APIRouter

from app.util.config.OpenApiDocumentation import Tags
from app.util.AzureCommonUtil import get_azure_scheme
from app.service.Pricing.Option.BaseOptionPricingService import OptionPriceResponse
from app.service.Pricing.Option.OptionPricingService import EuropeanOptionPriceRequest, \
    AmericanOptionPriceRequest, OptionPricingService

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


END_POINT_VANILLA_EUROPEAN = "/option/vanilla/european/calculation"
END_POINT_VANILLA_AMERICAN = "/option/vanilla/american/calculation"
END_POINT_BARRIER_EUROPEAN = "/option/barrier/european/calculation"


async def execute_calculation(option_request):
    logger.info('Pricing Request: {}'.format(option_request))
    price_response = OptionPricingService().execute(option_request)
    logger.info('Pricing Response: {}'.format(price_response))
    return price_response


@router.post(
    END_POINT_VANILLA_EUROPEAN,
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.option_pricing],
    summary="European Vanilla Option Calculation",
    response_description="Price Calculated",
    )
async def european_vanilla_calculation(option_request: EuropeanOptionPriceRequest) -> OptionPriceResponse:
    """
    Vanilla Option End-point is used to calculate Options with exercise type European.

    Uses **AnalyticEuropeanEngine**:
    * AnalyticEuropeanEngine is a pricing engine for European vanilla options using analytical formulae.
      It is used to calculate the price of an option using an analytical formula rather than a numerical
      method such as the binomial tree method.
      The formula used depends on the type of option being priced and the underlying asset’s price movement
      over time.

    - **Request body Schema**: EuropeanOptionRequest
    """
    return await execute_calculation(option_request)


@router.post(
    END_POINT_VANILLA_AMERICAN,
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.option_pricing],
    summary="American Vanilla Option Calculation",
    response_description="Price Calculated",
    )
async def american_vanilla_calculation(option_request: AmericanOptionPriceRequest) -> OptionPriceResponse:
    """
    Vanilla Option End-point is used to calculate Options with exercise type American.

    Uses **BinomialVanillaEngine**:
    * BinomialVanillaEngine is a pricing engine for vanilla options using binomial trees. It is used to
      calculate the price of an option by modeling the underlying asset’s price movement over time using
      a binomial tree.
      The tree is constructed by dividing time into discrete intervals and modeling the asset’s price
      movement as either an up or down movement at each interval.
      The price of the option is then calculated by working backwards through the tree from the final node
      to the initial node.

    - **Request body Schema**: AmericanOptionRequest
    """
    return await execute_calculation(option_request)

@router.post(
    END_POINT_BARRIER_EUROPEAN,
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.option_pricing],
    summary="European Barrier Option Calculation",
    response_description="Price Calculated",
    )
async def european_barrier_calculation(option_request: BarrierEuropeanOptionPriceRequest) -> OptionPriceResponse:
    """
    Vanilla Option End-point is used to calculate Options with exercise type European.

    Uses **AnalyticBarrierEngine**:
    * AnalyticBarrierEngine utilizes analytical formulas to calculate the prices and sensitivities of barrier
      options without the need for numerical methods or simulations.
    * It supports various types of barrier options, such as up-and-out, down-and-out, up-and-in, and down-and-in
    options.

    - **Request body Schema**: BarrierEuropeanOptionRequest
    """
    return await execute_calculation(option_request)
