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

from app.service.YieldCurve.YIeldCourveHelper import get_tenor, fetch_benchmark_points
from app.core.ApiSetting import ApiSettings
from app.service.Pricing.Option.EnumOptionPricingService import CountryInterestRateId
from app.service.YieldCurve.BaseYieldCurveService import BaseYieldCurveService, BenchmarkHelper, \
    MethodFactory
from app.service.YieldCurve.YieldCurveConfiguration import YieldCurveConfiguration
from app.util.QuantLibCommonUtil import get_today
from app.service.YieldCurve.EnumYieldCurveService import ZeroCurveMethod

import logging


class ZeroCurveMethodFactory(MethodFactory):
    def get_instance(self):
        return {
            ZeroCurveMethod.ZeroCurve: ql.ZeroCurve,
            ZeroCurveMethod.LogLinearZeroCurve: ql.LogLinearZeroCurve,
            ZeroCurveMethod.CubicZeroCurve: ql.CubicZeroCurve,
            ZeroCurveMethod.NaturalCubicZeroCurve: ql.NaturalCubicZeroCurve,
            ZeroCurveMethod.LogCubicZeroCurve: ql.LogCubicZeroCurve,
            ZeroCurveMethod.MonotonicCubicZeroCurve: ql.MonotonicCubicZeroCurve
        }


class ZeroCurveBenchmarkHelper(BenchmarkHelper):

    __DEFAULT_COUNTRY = CountryInterestRateId.SWITZERLAND

    def __init__(self, configuration: YieldCurveConfiguration):
        super().__init__(configuration)
        self.app_settings = ApiSettings()

    def build_rate_tenors(self, benchmark_points) -> tuple:
        tenors = []
        rates = []
        today = ql.Date().todaysDate()
        for point in benchmark_points['benchmark_points']:
            tenor = get_tenor(point['tenor'])
            rate = point.get('rate', None)
            if tenor is None or rate is None:
                continue
            tenors.append(today + tenor)
            rates.append(rate)
        return tenors, rates

    async def helper(self) -> tuple:
        benchmark_points = await fetch_benchmark_points(self.__DEFAULT_COUNTRY, #TODO has to be removed and received as parameter
                                                        self.app_settings)
        return self.build_rate_tenors(benchmark_points)


class ZeroCurveYieldCurveService(BaseYieldCurveService):
    
    def __init__(self):
        ql.Settings.instance().evaluationDate = get_today()
        configuration = YieldCurveConfiguration()
        super().__init__(configuration, ZeroCurveMethodFactory())
        self.__benchmark_helper = ZeroCurveBenchmarkHelper(configuration)

    async def get_helpers(self) -> tuple:
        return await self.__benchmark_helper.helper()

    async def get_params(self) -> list:
        tenors, rates = await self.get_helpers()
        return [tenors,
                rates,
                self.get_configuration().day_counter,
                self.get_configuration().calendar]
