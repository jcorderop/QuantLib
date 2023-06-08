"""
Created: 02.06.2023
Description:
    * This Modules defines the Option request that can be used.
"""
__author__ = "OE - JC"

from pydantic import StrictFloat

from app.service.Pricing.FixedIncome.EnumFixedIncomePricingService import SchedulePeriod
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from app.service.Pricing.FixedIncome.BaseFixedIncomePricingService import BaseFixedIncomePriceRequest

import logging

logger = logging.getLogger(__name__)


class ZeroBondPriceRequest(BaseFixedIncomePriceRequest):
    pass


class FixedBondPriceRequest(BaseFixedIncomePriceRequest):
    fixed_coupon: StrictFloat
    schedule_period: SchedulePeriod
