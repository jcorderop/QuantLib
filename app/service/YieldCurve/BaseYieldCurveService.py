"""
Created: 01.06.2023
Description:
    * This Module defines the classes used for the market data infrastructure.
"""
__author__ = "OE - JC"

from typing import Any

from app.util.QuantLibCommonUtil import get_date, get_today
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql
from abc import ABC, abstractmethod
from datetime import date
from pydantic import StrictFloat

from app.core.model.BaseModel import BaseObject
from app.service.YieldCurve.EnumYieldCurveService import PiecewiseMethod
from app.service.YieldCurve import YieldCurveConfiguration

import logging

logger = logging.getLogger(__name__)


class YieldCurveResponse(BaseObject):
    point_value: StrictFloat


class BenchmarkHelper(ABC):

    def __init__(self, configuration: YieldCurveConfiguration):
        self.__configuration = configuration

    @abstractmethod
    def helper(self) -> ql.RateHelperVector:
        ...

    def get_configuration(self) -> YieldCurveConfiguration:
        return self.__configuration


class MethodFactory(ABC):
    @abstractmethod
    def get_instance(self) -> dict:
        ...


class BaseYieldCurveService(ABC):
    
    def __init__(self,
                 configuration: YieldCurveConfiguration,
                 method_factory: MethodFactory):
        self.__configuration = configuration
        self.__method_factory = method_factory

    async def discount(self, method: PiecewiseMethod, target_date: date) -> YieldCurveResponse:
        instance = await self.get_instance(method)
        discount = instance.discount(get_date(target_date))
        return YieldCurveResponse(point_value=discount)

    async def zero_rate(self, method: PiecewiseMethod, target_date: date) -> YieldCurveResponse:
        instance = await self.get_instance(method)
        rate = instance.zeroRate(get_date(target_date),
                                 self.get_configuration().day_counter,
                                 self.get_configuration().compounding,
                                 self.get_configuration().compounding_frequency).rate()
        return YieldCurveResponse(point_value=rate)

    async def forward_rate(self, method: PiecewiseMethod, target_date: date) -> YieldCurveResponse:
        instance = await self.get_instance(method)
        print(get_today())
        print(get_date(target_date))
        rate = instance.forwardRate(get_today(), # TODO, most probably this date has to be changed
                                    get_date(target_date),
                                    self.get_configuration().day_counter,
                                    self.get_configuration().compounding_frequency).rate()
        return YieldCurveResponse(point_value=rate)

    @abstractmethod
    async def get_params(self) -> list:
        ...

    def get_configuration(self) -> YieldCurveConfiguration:
        return self.__configuration

    async def get_instance(self, method: PiecewiseMethod) -> Any:
        params = await self.get_params()
        return self.__method_factory.get_instance()[method](*params)



