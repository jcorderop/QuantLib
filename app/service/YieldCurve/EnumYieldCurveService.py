"""
Created: 01.06.2023
Description:
    * This Module defines the enum used for the market data infrastructure.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from enum import Enum

import logging

logger = logging.getLogger(__name__)


class ZeroCurveMethod(str, Enum):
    ZeroCurve = "ZeroCurve"
    LogLinearZeroCurve = "LogLinearZeroCurve"
    CubicZeroCurve = "CubicZeroCurve"
    NaturalCubicZeroCurve = "NaturalCubicZeroCurve"
    LogCubicZeroCurve = "LogCubicZeroCurve"
    MonotonicCubicZeroCurve = "MonotonicCubicZeroCurve"


class PiecewiseMethod(str, Enum):
    FlatForward = 'PiecewiseFlatForward'
    LogLinearDiscount = 'PiecewiseFlatForward'
    LogCubicDiscount = 'PiecewiseLogCubicDiscount'
    LinearZero = 'LinearZero'
    CubicZero = 'CubicZero'
    LinearForward = 'LinearForward'
    SplineCubicDiscount = 'SplineCubicDiscount'


class YieldCurveFunctions(str, Enum):
    forward_rate = 'forward_rate' # (today, target_date, day_counter, compounding_frequency).rate()
    discount = 'discount' # (target_date)
    zero_rate = 'zero_rate' # (target_date, day_counter, compounding_type, compounding_frequency).rate()

