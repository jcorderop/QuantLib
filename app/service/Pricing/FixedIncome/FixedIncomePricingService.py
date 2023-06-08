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
from datetime import datetime
from app.util.CommonApiUtil import rounding

from app.service.Pricing.FixedIncome.FixedIncomePayOff import FixedIncomePayOff, ZeroBondPayOffBuilder, FixedBondPayOffBuilder
from app.service.Pricing.PricingConfiguration import PricingConfiguration
from app.service.Pricing.FixedIncome.BaseFixedIncomePricingService import Pricer, PricingCalculationService, FixedIncomePriceResponse, AbstractFixedIncomeRequest
from app.core.ApiException import ApiException
from app.service.Pricing.FixedIncome.FixedIncomeRequest import ZeroBondPriceRequest, FixedBondPriceRequest

import logging

logger = logging.getLogger(__name__)


class BaseFixedIncomePricer(Pricer):

    __ROUNDING = 4

    def __init__(self, fixed_income_payoff: FixedIncomePayOff):
        ql.Settings.instance().evaluationDate = ql.Date.todaysDate()
        self.payoff = fixed_income_payoff

    def calculate_price(self) -> FixedIncomePriceResponse:
        fixed_income = self.build_fixed_income()
        engine = self.build_pricing_engine()
        fixed_income.setPricingEngine(engine)
        return FixedIncomePriceResponse(clean_price=rounding(fixed_income.cleanPrice()),
                                        dirty_price=rounding(fixed_income.dirtyPrice()),
                                        resp_datetime=datetime.now())

    @abstractmethod
    def build_fixed_income(self) -> ql.Instrument:
        ...

    def build_pricing_engine(self) -> ql.PricingEngine:
        flat_forward = ql.FlatForward(self.payoff.start_date,
                                      self.get_interest_rate(),
                                      self.payoff.day_counter,
                                      self.payoff.compounding,
                                      self.payoff.schedule_period.type())
        spot_curve_handle = ql.YieldTermStructureHandle(flat_forward)
        return ql.DiscountingBondEngine(spot_curve_handle)

    def get_interest_rate(self):
        return 0.05 # TODO integrate with endpoint


class ZeroBondPricer(BaseFixedIncomePricer):

    def __init__(self, payoff: FixedIncomePayOff):
        super().__init__(payoff)

    def build_fixed_income(self) -> ql.Instrument:
        return ql.ZeroCouponBond(
                self.payoff.settlement_days,
                self.payoff.calendar,
                self.payoff.face_amount,
                self.payoff.end_date,
                self.payoff.convention,
                self.payoff.redemption_amount,
                self.payoff.start_date,
            )


class FixedBondPricer(BaseFixedIncomePricer):

    def __init__(self, payoff: FixedIncomePayOff):
        super().__init__(payoff)

    def build_fixed_income(self) -> ql.Instrument:
        schedule = ql.Schedule(
                self.payoff.start_date,
                self.payoff.end_date,
                ql.Period(self.payoff.schedule_period.type()),
                self.payoff.calendar,
                ql.Unadjusted,
                ql.Unadjusted,
                ql.DateGeneration.Backward,
                False,
            )

        return ql.FixedRateBond(
            self.payoff.settlement_days,
            self.payoff.face_amount,
            schedule,
            [self.payoff.fixed_coupon],
            self.payoff.day_counter,
            self.payoff.convention,
            self.payoff.redemption_amount,
            self.payoff.start_date,
        )


class FixedIncomePricingService(PricingCalculationService):

    @staticmethod
    def __fixed_income_pricer_factory(price_request: AbstractFixedIncomeRequest,
                                      configuration: PricingConfiguration) -> BaseFixedIncomePricer:
        if isinstance(price_request, ZeroBondPriceRequest):
            payoff = ZeroBondPayOffBuilder().build_payoff(price_request,
                                                          configuration)
            return ZeroBondPricer(payoff)
        if isinstance(price_request, FixedBondPriceRequest):
            payoff = FixedBondPayOffBuilder().build_payoff(price_request,
                                                           configuration)
            return FixedBondPricer(payoff)
        else:
            raise ApiException('Invalid pricing request type...')

    @staticmethod
    def __fixed_income_factory(price_request: AbstractFixedIncomeRequest) -> BaseFixedIncomePricer:
        configuration = PricingConfiguration()
        return FixedIncomePricingService.__fixed_income_pricer_factory(price_request, configuration)

    def execute(self, price_request: AbstractFixedIncomeRequest) -> FixedIncomePriceResponse:
        vanilla_option = FixedIncomePricingService.__fixed_income_factory(price_request)
        logger.info('Using Pricing: {}'.format(vanilla_option))
        return vanilla_option.calculate_price()

