"""
Created: 01.06.2023
Description:
    * This Module defines the configuration used for the yield curve infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from app.util.config.ValuationConfiguration import ValuationConfiguration


class YieldCurveConfiguration:
    compounding_frequency = ValuationConfiguration.compounding_frequency
    calendar = ValuationConfiguration.calendar
    convention = ValuationConfiguration.convention
    day_counter = ValuationConfiguration.day_counter
    compounding_type = ValuationConfiguration.compounding_type
    end_of_month = ValuationConfiguration.end_of_month
    fixing_days = ValuationConfiguration.fixing_days