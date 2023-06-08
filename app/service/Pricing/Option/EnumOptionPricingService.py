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


class CountryInterestRateId(Enum):
    SWITZERLAND = 'switzerland'


class OptionTypeEnum(str, Enum):
    CALL = 'call'
    PUT = 'put'

    def type(self):
        return {
                self.CALL: 1,
                self.PUT: -1,
            }[self]


class BarrierTypeEnum(str, Enum):
    UP_AND_IN = 'up-and-in'
    UP_AND_OUT = 'up-and-out'
    DOWN_AND_IN = 'down-and-in'
    DOWN_AND_OUT = 'down-and-out'

    def type(self):
        return {
                self.DOWN_AND_IN: 0,
                self.DOWN_AND_OUT: 2,
                self.UP_AND_IN: 1,
                self.UP_AND_OUT: 3
            }[self]


class OptionFeatureNameEnum(str, Enum):
    BARRIER_OPTION = 'barrier_option'


class ExerciseTypeEnum(str, Enum):
    EUROPEAN = 'european'
    AMERICAN = 'american'


class BinomialEngineTypeEnum(str, Enum):
    TypeBinomialCRRVanillaEngine = "crr"
    TypeBinomialJRVanillaEngine = "jr"
    TypeBinomialEQPVanillaEngine = "eqp"
    TypeBinomialTrigeorgisVanillaEngine = "trigeorgis"
    TypeBinomialTianVanillaEngine = "tian"
    TypeBinomialLRVanillaEngine = "lr"
    TypeBinomialJ4VanillaEngine = "j4"