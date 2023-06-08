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
from pydantic import StrictFloat, Field, BaseModel

from app.core.model.BaseModel import BaseObject


class Pricer(ABC):

    @abstractmethod
    def calculate_price(self):
        ...


class FixedIncomePriceResponse(BaseObject):
    clean_price: StrictFloat
    dirty_price: StrictFloat
    resp_datetime: datetime


class AbstractFixedIncomeRequest(ABC):
    pass


class BaseFixedIncomePriceRequest(BaseModel, AbstractFixedIncomeRequest):
    _created_at: datetime = Field(default_factory=datetime.now)

    start_date: date = Field(description="Start Date")
    end_date: date = Field(description="End Date")



class PricingCalculationService(ABC):

    @abstractmethod
    def execute(self, price_request: AbstractFixedIncomeRequest):
        ...
