"""
Created: 01.06.2023
Description:
    * This Service is designed to provide yield curve data.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
import QuantLib as ql

from app.service.YieldCurve.YIeldCourveHelper import fetch_benchmark_points, get_tenor
from app.core.ApiSetting import ApiSettings
from app.service.Pricing.Option.EnumOptionPricingService import CountryInterestRateId
from app.service.YieldCurve.BaseYieldCurveService import BaseYieldCurveService, BenchmarkHelper, \
    MethodFactory
from app.service.YieldCurve.EnumYieldCurveService import PiecewiseMethod
from app.service.YieldCurve.YieldCurveConfiguration import YieldCurveConfiguration
from app.util.QuantLibCommonUtil import get_today

import logging

logger = logging.getLogger(__name__)


class PiecewiseMethodFactory(MethodFactory):
    def get_instance(self):
        return {
            PiecewiseMethod.FlatForward: ql.PiecewiseFlatForward,
            PiecewiseMethod.LogLinearDiscount: ql.PiecewiseLogLinearDiscount,
            PiecewiseMethod.LogCubicDiscount: ql.PiecewiseLogCubicDiscount,
            PiecewiseMethod.LinearZero: ql.PiecewiseLinearZero,
            PiecewiseMethod.CubicZero: ql.PiecewiseCubicZero,
            PiecewiseMethod.LinearForward: ql.PiecewiseLinearForward,
            PiecewiseMethod.SplineCubicDiscount: ql.PiecewiseSplineCubicDiscount
        }


class DepositBenchmarkHelper(BenchmarkHelper):

    __DEFAULT_COUNTRY = CountryInterestRateId.SWITZERLAND

    def __init__(self, configuration: YieldCurveConfiguration):
        super().__init__(configuration)
        self.app_settings = ApiSettings()

    def build_deposits(self, benchmark_points) -> ql.RateHelperVector:
        helpers = ql.RateHelperVector()
        for point in benchmark_points['benchmark_points']:
            tenor = get_tenor(point['tenor'])
            rate = point.get('rate', None)
            if tenor is None or rate is None:
                continue
            helpers.append(ql.DepositRateHelper(rate,
                                                tenor,
                                                self.get_configuration().fixing_days,
                                                self.get_configuration().calendar,
                                                self.get_configuration().convention,
                                                self.get_configuration().end_of_month,
                                                self.get_configuration().day_counter))
        return helpers

    async def helper(self) -> ql.RateHelperVector:
        benchmark_points = await fetch_benchmark_points(self.__DEFAULT_COUNTRY, #TODO has to be removed and received as parameter
                                                             self.app_settings)
        return self.build_deposits(benchmark_points)


class PiecewiseYieldCurveService(BaseYieldCurveService):

    def __init__(self):
        ql.Settings.instance().evaluationDate = get_today()
        configuration = YieldCurveConfiguration()
        super().__init__(configuration, PiecewiseMethodFactory())
        self.__benchmark_instruments = DepositBenchmarkHelper(configuration)

    async def get_helpers(self) -> ql.RateHelperVector:
        return await self.__benchmark_instruments.helper()

    async def get_params(self) -> list:
        return [self.get_configuration().fixing_days,
                self.get_configuration().calendar,
                await self.get_helpers(),
                self.get_configuration().day_counter]
