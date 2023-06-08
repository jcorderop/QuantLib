"""
Created: 22.05.2023
Description:
    * This Library offers common functionality used for the application in relation with QuantLib.
"""
__author__ = "OE - JC"

from app.service.Pricing.Option.EnumOptionPricingService import OptionTypeEnum
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from datetime import datetime, date
import QuantLib as ql


def get_today() -> ql.Date:
    today = datetime.now().date()
    return ql.Date(today.day, today.month, today.year)


def get_date(target_date: date) -> ql.Date:
    return ql.Date(target_date.day, target_date.month, target_date.year)