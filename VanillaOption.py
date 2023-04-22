# https://docs.pydantic.dev/usage/types/#enums-and-choices
# http://gouthamanbalaraman.com/blog/american-option-pricing-quantlib-python.html

from enum import Enum

import QuantLib as ql
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, StrictFloat, validator


class OptionTypeEnum(str, Enum):
    CALL = 'call'
    PUT = 'put'


class ExerciseTypeEnum(str, Enum):
    EUROPEAN = 'european'
    AMERICAN = 'american'


class OptionRequest(BaseModel):
    calculation_date: date
    maturity_date: date
    spot_price: StrictFloat
    strike_price: StrictFloat
    volatility: StrictFloat
    dividend_rate: StrictFloat
    risk_free_rate: StrictFloat
    option_type: OptionTypeEnum
    exercise_type: ExerciseTypeEnum

    @validator('option_type')
    def is_option_type_enum(cls, option_type):
        if option_type not in [OptionTypeEnum.CALL, OptionTypeEnum.PUT]:
            raise ValueError('must contain a space')
        return option_type

    def get_calculation_date(self):
        return ql.Date(self.calculation_date.day,
                       self.calculation_date.month,
                       self.calculation_date.year)

    def get_maturity_date(self):
        return ql.Date(self.maturity_date.day,
                       self.maturity_date.month,
                       self.maturity_date.year)

    def get_option_type(self):
        if OptionTypeEnum.CALL == self.option_type:
            return ql.Option.Call
        else:
            return ql.Option.Put


def vanilla_option_calculation(op_req: OptionRequest):
    calculation_date = op_req.get_calculation_date()
    maturity_date = op_req.get_maturity_date()
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
    ql.Settings.instance().evaluationDate = calculation_date

    payoff = ql.PlainVanillaPayoff(op_req.get_option_type(), op_req.strike_price)
    settlement = calculation_date

    am_exercise = ql.AmericanExercise(settlement, maturity_date)
    american_option = ql.VanillaOption(payoff, am_exercise)

    eu_exercise = ql.EuropeanExercise(maturity_date)
    european_option = ql.VanillaOption(payoff, eu_exercise)

    spot_handle = ql.QuoteHandle(ql.SimpleQuote(op_req.spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, op_req.risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, op_req.dividend_rate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, op_req.volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle,
                                               dividend_yield,
                                               flat_ts,
                                               flat_vol_ts)

    steps = 200
    binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)

    if op_req.exercise_type.EUROPEAN:
        european_option.setPricingEngine(binomial_engine)
        return european_option.NPV()
    else:
        american_option.setPricingEngine(binomial_engine)
        return american_option.NPV()


if __name__ == '__main__':
    # option data
    op_req = OptionRequest(calculation_date=datetime.now(),
                           maturity_date=datetime.now() + relativedelta(years=+1),
                           spot_price=127.62,
                           strike_price=130.0,
                           volatility=0.20, # the historical vols or implied vols
                           dividend_rate=0.0163,
                           risk_free_rate=0.001,
                           option_type=OptionTypeEnum.CALL,
                           exercise_type=ExerciseTypeEnum.AMERICAN)

    print(op_req)
    price = vanilla_option_calculation(op_req)
    print('option price: {}'.format(price))