"""
Created: 22.05.2023
Description:
    * This Service is designed to price Vanilla Option with European and America exercise style.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from abc import abstractmethod
import QuantLib as ql
from QuantLib import Exercise
from datetime import datetime
from app.util.CommonApiUtil import rounding

from app.service.Pricing.Option.OptionPayOff import OptionPayOff, build_option_payoff
from app.service.Pricing.PricingConfiguration import PricingConfiguration
from app.service.Pricing.Option.BaseOptionPricingService import AbstractOptionRequest, Pricer, OptionPriceResponse, \
    PricingCalculationService
from app.service.Pricing.Option.EnumOptionPricingService import BinomialEngineTypeEnum, OptionFeatureNameEnum
from app.core.ApiException import ApiException
from app.service.Pricing.Option.OptionRequest import AmericanOptionPriceRequest, BarrierEuropeanOptionPriceRequest, EuropeanOptionPriceRequest

import logging

logger = logging.getLogger(__name__)


def get_greek_value(option_callback, dp: int) -> float:
    try:
        return rounding(option_callback(), dp)
    except:
        return 0.0


class BaseOptionPricer(Pricer):

    __ROUNDING = 4

    def __init__(self, option_payoff: OptionPayOff):
        ql.Settings.instance().evaluationDate = ql.Date.todaysDate()
        self.option_payoff = option_payoff

    def calculate_price(self) -> OptionPriceResponse:
        price_engine = self.build_pricing_engine()
        option = self.get_option()
        option.setPricingEngine(price_engine)
        return OptionPriceResponse(option_price=rounding(option.NPV(), self.__ROUNDING),
                                   delta=get_greek_value(option.delta, self.__ROUNDING),
                                   gamma=get_greek_value(option.gamma, self.__ROUNDING),
                                   theta=get_greek_value(option.theta, self.__ROUNDING),
                                   vega=get_greek_value(option.vega, self.__ROUNDING),
                                   resp_datetime=datetime.now())

    @abstractmethod
    def get_exercise(self) -> float:
        ...

    @abstractmethod
    def build_pricing_engine(self) -> ql.PricingEngine:
        ...

    def get_quote_handler(self):
        return ql.QuoteHandle(ql.SimpleQuote(self.option_payoff.spot_price))

    def get_volatility_structure(self):
        return ql.BlackVolTermStructureHandle(ql.BlackConstantVol(self.option_payoff.issue_date,
                                                                  self.option_payoff.calendar,
                                                                  self.option_payoff.volatility,
                                                                  self.option_payoff.day_counter))

    def get_risk_free_rate_structure(self):
        return ql.YieldTermStructureHandle(ql.FlatForward(self.option_payoff.issue_date,
                                                          self.option_payoff.risk_free_rate,
                                                          self.option_payoff.day_counter))

    def get_dividend_structure(self):
        return ql.YieldTermStructureHandle(ql.FlatForward(self.option_payoff.issue_date,
                                                          self.option_payoff.dividend_rate,
                                                          self.option_payoff.day_counter))

    def get_payoff(self) -> ql.PlainVanillaPayoff:
        return ql.PlainVanillaPayoff(self.option_payoff.option_type, self.option_payoff.strike_price)

    def get_option(self) -> ql.Instrument:
        return ql.VanillaOption(self.get_payoff(), self.get_exercise())

    def get_process(self) -> ql.BlackScholesMertonProcess:
        return ql.BlackScholesMertonProcess(self.get_quote_handler(),
                                            self.get_dividend_structure(),
                                            self.get_risk_free_rate_structure(),
                                            self.get_volatility_structure())


class VanillaOptionEuropeanPricer(BaseOptionPricer):

    def get_exercise(self) -> Exercise:
        return ql.EuropeanExercise(self.option_payoff.maturity_date)

    def build_pricing_engine(self) -> ql.PricingEngine:
        return ql.AnalyticEuropeanEngine(self.get_process())


class BarrierOptionEuropeanPricer(VanillaOptionEuropeanPricer):

    def get_option(self) -> ql.Instrument:
        feature = self.option_payoff.get_feature(OptionFeatureNameEnum.BARRIER_OPTION)
        return ql.BarrierOption(feature.barrier_type,
                                feature.barrier_price,
                                feature.rebate,
                                self.get_payoff(), 
                                self.get_exercise())

    def build_pricing_engine(self) -> ql.PricingEngine:
        return ql.FdBlackScholesBarrierEngine(self.get_process())


class VanillaOptionAmericanPricer(BaseOptionPricer):

    def __init__(self, payoff: OptionPayOff,
                 engine_type: BinomialEngineTypeEnum,
                 steps: int):
        super().__init__(payoff)
        self.engine_type = engine_type
        self.steps = steps

    def get_exercise(self) -> Exercise:
        return ql.AmericanExercise(self.option_payoff.issue_date, self.option_payoff.maturity_date)

    def build_pricing_engine(self) -> ql.PricingEngine:
        return ql.BinomialVanillaEngine(self.get_process(), self.engine_type, self.steps)


class OptionPricingService(PricingCalculationService):

    @staticmethod
    def __option_pricer_factory(price_request: AbstractOptionRequest,
                                configuration: PricingConfiguration) -> BaseOptionPricer:
        payoff = build_option_payoff(price_request,
                                     configuration)

        if isinstance(price_request, BarrierEuropeanOptionPriceRequest):
            return BarrierOptionEuropeanPricer(payoff)
        if isinstance(price_request, AmericanOptionPriceRequest):
            return VanillaOptionAmericanPricer(payoff,
                                               price_request.engine_type,
                                               price_request.steps)
        if isinstance(price_request, EuropeanOptionPriceRequest):
            return VanillaOptionEuropeanPricer(payoff)
        else:
            raise ApiException('Invalid pricing request type...')

    @staticmethod
    def __option_factory(price_request: AbstractOptionRequest) -> BaseOptionPricer:
        configuration = PricingConfiguration()
        return OptionPricingService.__option_pricer_factory(price_request, configuration)

    def execute(self, price_request: AbstractOptionRequest) -> OptionPriceResponse:
        vanilla_option = OptionPricingService.__option_factory(price_request)
        logger.info('Using Pricing: {}'.format(vanilla_option))
        return vanilla_option.calculate_price()

