"""
Created: 02.06.2023
Description:
    * This Modules defines the Option Payoff template.
"""
__author__ = "OE - JC"

from abc import ABC, abstractmethod
from typing import Optional

from app.service.Pricing.FixedIncome.EnumFixedIncomePricingService import SchedulePeriod
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql
from pydantic import Field, StrictFloat
from datetime import datetime

from app.core.model.BaseModel import BaseObject
from app.service.Pricing.FixedIncome.BaseFixedIncomePricingService import BaseFixedIncomePriceRequest
from app.service.Pricing.PricingConfiguration import PricingConfiguration
from app.util.QuantLibCommonUtil import get_date

import logging

logger = logging.getLogger(__name__)


class FixedIncomePayOff(BaseObject):
    created_at: datetime = Field(default_factory=datetime.now)

    start_date: ql.Date = Field(description="Start Date")
    end_date: ql.Date = Field(description="End Date")

    # TODO decouple quantlib
    calendar: ql.Calendar = None
    day_counter: ql.DayCounter = None
    convention: int
    compounding: int
    settlement_days: int

    face_amount: int = 1
    redemption_amount: int = 100

    fixed_coupon: Optional[StrictFloat] = None
    schedule_period: Optional[SchedulePeriod] = SchedulePeriod.QUARTERLY

    class Config:
        arbitrary_types_allowed = True


def get_value(price_request: BaseFixedIncomePriceRequest, field_name: str):
    if hasattr(price_request, field_name):
        return price_request.__getattribute__(field_name)


class BaseFixedIncomePayOffBuilder(ABC):
    @abstractmethod
    def build_payoff(self,
                     price_request: BaseFixedIncomePriceRequest,
                     configuration: PricingConfiguration) -> FixedIncomePayOff:
        ...


class ZeroBondPayOffBuilder(BaseFixedIncomePayOffBuilder):

    def build_payoff(self,
                     price_request: BaseFixedIncomePriceRequest,
                     configuration: PricingConfiguration) -> FixedIncomePayOff:
        return FixedIncomePayOff(start_date=get_date(price_request.start_date),
                                 end_date=get_date(price_request.end_date),

                                 calendar=configuration.calendar,
                                 day_counter=configuration.day_counter,
                                 convention=configuration.convention,
                                 compounding=configuration.compounding,
                                 settlement_days=configuration.settlement_days
                                 )


class FixedBondPayOffBuilder(BaseFixedIncomePayOffBuilder):

    def build_payoff(self,
                     price_request: BaseFixedIncomePriceRequest,
                     configuration: PricingConfiguration) -> FixedIncomePayOff:
        return FixedIncomePayOff(start_date=get_date(price_request.start_date),
                                 end_date=get_date(price_request.end_date),

                                 calendar=configuration.calendar,
                                 day_counter=configuration.day_counter,
                                 convention=configuration.convention,
                                 compounding=configuration.compounding,
                                 settlement_days=configuration.settlement_days,

                                 fixed_coupon=get_value(price_request, 'fixed_coupon'),
                                 schedule_period=get_value(price_request, 'schedule_period'),
                                 )