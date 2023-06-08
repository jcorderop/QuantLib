"""
Created: 02.06.2023
Description:
    * This Modules defines the Option request that can be used.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from typing import Optional
from pydantic import StrictInt, StrictFloat, BaseModel

from app.service.Pricing.Option.BaseOptionPricingService import BaseOptionPriceRequest
from app.service.Pricing.Option.EnumOptionPricingService import ExerciseTypeEnum, BinomialEngineTypeEnum, BarrierTypeEnum

import logging

logger = logging.getLogger(__name__)


class EuropeanOptionPriceRequest(BaseOptionPriceRequest):

    def get_exersice_type(self) -> ExerciseTypeEnum:
        return ExerciseTypeEnum.EUROPEAN


class BarrierOption(BaseModel):
    barrier_price: StrictFloat
    barrier_type: BarrierTypeEnum

    class Config:
        arbitrary_types_allowed = True


class BarrierEuropeanOptionPriceRequest(EuropeanOptionPriceRequest):
    barrier: BarrierOption

    class Config:
        arbitrary_types_allowed = True


class AmericanOptionPriceRequest(BaseOptionPriceRequest):
    engine_type: Optional[BinomialEngineTypeEnum] = BinomialEngineTypeEnum.TypeBinomialCRRVanillaEngine
    steps: Optional[StrictInt] = 200

    def get_exersice_type(self) -> ExerciseTypeEnum:
        return ExerciseTypeEnum.AMERICAN
