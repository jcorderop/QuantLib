"""
Created: 22.05.2023
Description:
    * This Module defines the classes used for pricing the infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional
from pydantic import StrictFloat, Field, validator, BaseModel

from app.service.Pricing.Option.EnumOptionPricingService import OptionTypeEnum, OptionFeatureNameEnum
from app.core.model.BaseModel import BaseObject


class Pricer(ABC):

    @abstractmethod
    def calculate_price(self):
        ...


class OptionPriceResponse(BaseObject):
    option_price: StrictFloat
    delta: Optional[StrictFloat] = Field(description="Measures impact of a change in the price of **underlying**. It moves between [0, -1] (put) and [1, 0] (call) and it can be used as probability to get in-the-money and if Delta moves in the oposit limits from 0 respectively the option get in-the-money.")
    gamma: Optional[StrictFloat] = Field(description="Measures the rate of change of **delta**. High gamma mean volatile underlying and low probability to expire in-the-money.")
    theta: Optional[StrictFloat] = Field(description="Measures impact of a change in **time** remaining. Theta is always negative for a single option.")
    vega: Optional[StrictFloat] = Field(description="Measures impact of a change in **volatility**. Vega can increase or decrease without price changes of the underlying asset, due to changes in implied volatility. Vega can increase in reaction to quick moves in the underlying asset. Vega falls as the option gets closer to expiration.")
    resp_datetime: datetime


class AbstractOptionRequest(ABC):
    @abstractmethod
    def get_exersice_type(self):
        ...


class BaseOptionPriceRequest(BaseModel, AbstractOptionRequest, ABC):
    _created_at: datetime = Field(default_factory=datetime.now)

    issue_date: date = Field(description="Issuing Date")
    maturity_date: date = Field(description="Expiry Date")

    spot_price: StrictFloat
    strike_price: StrictFloat
    volatility: StrictFloat = Field(description="Constant Volatility")
    risk_free_rate: StrictFloat = Field(description="Risk Free Ratio based on the Underlying Currency")
    dividend_rate: StrictFloat

    option_type: OptionTypeEnum

    @validator('option_type')
    def is_option_type_enum(cls, option_type) -> bool:
        if option_type not in [OptionTypeEnum.CALL, OptionTypeEnum.PUT]:
            raise ValueError('must contain a space')
        return option_type


class PricingCalculationService(ABC):

    @abstractmethod
    def execute(self, price_request: AbstractOptionRequest):
        ...


class BaseFeature(BaseObject):
    name: str

    class Config:
        arbitrary_types_allowed = True