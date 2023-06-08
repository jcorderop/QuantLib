"""
Created: 22.05.2023
Description:
    * This Module defines the enum used for pricing the infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from enum import Enum
import QuantLib as ql


class SchedulePeriod(str, Enum):
    QUARTERLY = "quarterly"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    BIMONTHLY = "bimonthly"
    SEMIANUAL = "semianual"
    ANUAL = "anual"

    def type(self):
        return {
                self.WEEKLY: ql.Weekly,
                self.BIWEEKLY: ql.Biweekly,
                self.MONTHLY: ql.Monthly,
                self.BIMONTHLY: ql.Bimonthly,
                self.QUARTERLY: ql.Quarterly,
                self.SEMIANUAL: ql.Semiannual,
                self.ANUAL: ql.Annual
            }[self]