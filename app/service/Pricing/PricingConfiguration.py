"""
Created: 01.06.2023
Description:
    * This Module defines the configuration used for the pricing infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql
from app.util.config.ValuationConfiguration import ValuationConfiguration


class PricingConfiguration:
    calendar = ValuationConfiguration.calendar
    day_counter = ValuationConfiguration.day_counter

    convention = ql.ModifiedFollowing
    compounding = ql.Continuous
    settlement_days = 2
