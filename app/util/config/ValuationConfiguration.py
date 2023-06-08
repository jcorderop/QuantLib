"""
Created: 01.06.2023
Description:
    * This Module defines the configuration used for the valuation module infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql


class ValuationConfiguration: # TODO, Configuration can be changed to loaded it dynamically or central place
    # TODO, has to be decouple the dependencies from Quantlib on the field types
    calendar: ql.Calendar = ql.Switzerland()  # TODO, review what actually Swiss calendar does
    day_counter: ql.DayCounter = ql.Actual360()
    compounding_frequency: int = ql.Annual
    convention: int = ql.ModifiedFollowing
    compounding_type: int = ql.Continuous
    end_of_month: bool = False
    fixing_days: int = 0