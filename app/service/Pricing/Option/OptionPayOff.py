"""
Created: 02.06.2023
Description:
    * This Modules defines the Option Payoff template.
"""
__author__ = "OE - JC"

from datetime import datetime

from app.core.ApiException import ApiException
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql
from pydantic import Field, StrictFloat
from typing import Optional

from app.core.model.BaseModel import BaseObject
from app.service.Pricing.Option.BaseOptionPricingService import BaseOptionPriceRequest, BaseFeature
from app.service.Pricing.Option.EnumOptionPricingService import ExerciseTypeEnum, OptionFeatureNameEnum
from app.service.Pricing.PricingConfiguration import PricingConfiguration
from app.util.QuantLibCommonUtil import get_date

import logging

logger = logging.getLogger(__name__)


class BarrierOptionFeature(BaseFeature):
    barrier_price: StrictFloat
    barrier_type: int = Field(description="Barrier type DownIn = 0, DownOut = 2, UpIn = 1, UpOut = 3") # TODO change it to an enum
    rebate: Optional[StrictFloat] = 0.0


def add_barrier_option(price_request: BaseOptionPriceRequest) -> BaseFeature:
    if hasattr(price_request, 'barrier'):
        return BarrierOptionFeature(name=OptionFeatureNameEnum.BARRIER_OPTION.value,
                                    barrier_price=price_request.barrier.barrier_price,
                                    barrier_type=price_request.barrier.barrier_type.type())


def add_features(price_request: BaseOptionPriceRequest) -> list[BaseFeature]:
    features = [add_barrier_option(price_request)]
    return list(filter(lambda x: x is not None, features))


class OptionPayOff(BaseObject):
    created_at: datetime = Field(default_factory=datetime.now)

    issue_date: ql.Date = Field(description="Issuing Date")
    maturity_date: ql.Date = Field(description="Expiry Date")

    spot_price: StrictFloat
    strike_price: StrictFloat
    risk_free_rate: StrictFloat = Field(description="Risk Free Ratio based on the Underlying Currency")
    dividend_rate: StrictFloat
    volatility: StrictFloat = Field(description="Constant Volatility")

    option_type: int = Field(description="Option type call 1 and put -1") # TODO change it to an enum
    exercise_type: ExerciseTypeEnum

    option_features: Optional[list[BaseFeature]]

    # TODO decouple quantlib
    calendar: ql.Calendar = None
    day_counter: ql.DayCounter = None

    def get_feature(self, feature_name: OptionFeatureNameEnum):
        features = list(filter(lambda feature: feature.name == feature_name, self.option_features))
        if features and len(features) > 0:
            return features[0]
        else:
            raise ApiException(f'Feature {feature_name.value} was not defined.')

    class Config:
        arbitrary_types_allowed = True


def build_option_payoff(price_request: BaseOptionPriceRequest,
                        configuration: PricingConfiguration) -> OptionPayOff:
    return OptionPayOff(issue_date=get_date(price_request.issue_date),
                        maturity_date=get_date(price_request.maturity_date),

                        spot_price=price_request.spot_price,
                        strike_price=price_request.strike_price,
                        risk_free_rate=price_request.risk_free_rate,
                        dividend_rate=price_request.dividend_rate,
                        volatility=price_request.volatility,

                        option_type=price_request.option_type.type(),
                        exercise_type=price_request.get_exersice_type(),

                        calendar=configuration.calendar,
                        day_counter=configuration.day_counter,

                        option_features=add_features(price_request)
                        )