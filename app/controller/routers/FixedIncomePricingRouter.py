"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for the pricing End-Points.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import Security, APIRouter
from app.util.config.OpenApiDocumentation import Tags
from app.util.AzureCommonUtil import get_azure_scheme

from app.service.Pricing.FixedIncome.BaseFixedIncomePricingService import FixedIncomePriceResponse
from app.service.Pricing.FixedIncome.FixedIncomePricingService import FixedIncomePricingService
from app.service.Pricing.FixedIncome.FixedIncomeRequest import ZeroBondPriceRequest, FixedBondPriceRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


END_POINT_ZERO_COUPON_BOND = "/fixed_income/zerocouponbond/calculation"
END_POINT_FIXED_COUPON_BOND = "/fixed_income/fixedcouponbond/calculation"


async def execute_calculation(price_request):
    logger.info('Pricing Request: {}'.format(price_request))
    price_response = FixedIncomePricingService().execute(price_request)
    logger.info('Pricing Response: {}'.format(price_response))
    return price_response


@router.post(
    END_POINT_ZERO_COUPON_BOND,
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.fixed_income_pricing],
    summary="Zero Coupon Bond Calculation",
    response_description="Price Calculated",
    )
async def zero_bond_calculation(price_request: ZeroBondPriceRequest) -> FixedIncomePriceResponse:
    """
    Zero Coupon Bond End-point.

    - **Request body Schema**: ZeroBondPriceRequest
    """
    return await execute_calculation(price_request)


@router.post(
    END_POINT_FIXED_COUPON_BOND,
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.fixed_income_pricing],
    summary="Fixed Coupon Bond Calculation",
    response_description="Price Calculated",
    )
async def american_vanilla_calculation(price_request: FixedBondPriceRequest) -> FixedIncomePriceResponse:
    """
    Fixed Coupon Bond End-point.

    - **Request body Schema**: FixedBondPriceRequest
    * Valid Schedule periods:
    ['weekly', 'biweekly', 'monthly', 'bimonthly', 'quarterly', 'semianual', 'anual']
    """
    return await execute_calculation(price_request)
