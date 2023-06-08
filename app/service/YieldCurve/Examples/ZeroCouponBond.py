from datetime import datetime

import QuantLib as ql
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

from app.service.Pricing.Option.EnumOptionPricingService import OptionTypeEnum

from scipy.optimize import fsolve
import logging

from app.service.Pricing.Option.OptionRequest import EuropeanOptionPriceRequest
from app.service.Pricing.Option.OptionPricingService import OptionPricingService
from app.util.QuantLibCommonUtil import get_date

logger = logging.getLogger(__name__)


def create_yield_curve(issue_date, maturity_Date):
    spot_dates = [issue_date + ql.Period(i, ql.Years) for i in range(10)]
    spot_rates = [0.018, 0.0189, 0.0192, 0.0198, 0.0215, 0.0218, 0.0224, 0.0226, 0.0229, 0.0235]

    day_count = ql.Actual360()
    calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
    #interpolation = ql.Linear()
    interpolation = ql.Cubic()
    compounding = ql.Compounded
    compounding_frequency = ql.Annual
    spot_curve = ql.CubicZeroCurve(spot_dates,
                              spot_rates,
                              day_count,
                              calendar,
                              interpolation,
                              ql.Continuous,#compounding,
                              compounding_frequency)
    print(len(spot_dates))
    print(len(spot_rates))
    print(day_count)
    print(calendar)
    print(interpolation)
    print(ql.Continuous)
    print(compounding_frequency)

    for node in spot_curve.nodes():
        print(node)

    dates = [date for date in spot_curve.dates()]
    dates_rate = []
    zeroRates = []
    #couponFrequency = ql.Semiannual
    for d in dates:
        years = day_count.yearFraction(issue_date, d)
        zeroRate = spot_curve.zeroRate(d, day_count, ql.Continuous, compounding_frequency).rate()
        zeroRates.append(zeroRate * 100)
        dates_rate.append(datetime(d.year(), d.month(), d.dayOfMonth()))

    print('zeroRates: {}'.format(zeroRates))
    print('dates: {}'.format(dates_rate))

    target_day = maturity_Date#ql.Date(30, 8, 2025)
    my_zero_rate = spot_curve.zeroRate(target_day, day_count, ql.Continuous, compounding_frequency).rate()
    print('zeroRate {}'.format(my_zero_rate))

    next_day = issue_date
    last_day = spot_dates[-1]
    zeroRates2 = []
    dates2 = []
    print(next_day)
    print(last_day)
    while next_day < last_day:
        zeroRate = spot_curve.zeroRate(next_day, day_count, ql.Continuous, compounding_frequency).rate()
        zeroRates2.append(zeroRate * 100)
        dates2.append(datetime(next_day.year(), next_day.month(), next_day.dayOfMonth()))
        next_day = next_day + 1



    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(dates2, zeroRates2, '-')
    ax.plot_date(dates_rate, zeroRates, '*')
    ax.plot_date([datetime(target_day.year(), target_day.month(), target_day.dayOfMonth())], [my_zero_rate * 100], 'o')
    plt.show()

    return spot_curve


def calculate_zero_bond(option_request):
    # Set up the bond parameters

    face_value = 1
    redemption = 100
    issue_date = get_date(option_request.issue_date)
    maturity_date = get_date(option_request.maturity_date)
    interest_rate = 0.018
    settlement_days = 0
    day_count = ql.Actual360()
    calendar = ql.UnitedStates(ql.UnitedStates.Settlement)

    ql.Settings.instance().evaluationDate = issue_date

    # Create a bond object

    bond = ql.ZeroCouponBond(settlement_days,
                             calendar,
                             face_value,
                             maturity_date,
                             ql.ModifiedFollowing,
                             redemption,
                             issue_date)

    # Set up the bond engine

    #qflatforw = ql.FlatForward(issue_date, interest_rate, ql.ActualActual(ql.ActualActual.ISMA), ql.Compounded,ql.Annual)
    qflatforw = create_yield_curve(issue_date, maturity_date)
    spot_curve_handle = ql.YieldTermStructureHandle(qflatforw)
    bond_engine = ql.DiscountingBondEngine(spot_curve_handle)

    # Assign the bond engine to the bond object

    bond.setPricingEngine(bond_engine)

    # Calculate the bond price

    cleanPrice = bond.cleanPrice()
    print(f"The clean_price of the bond is: {cleanPrice:.2f}")

    dirtyPrice = bond.dirtyPrice()
    print(f"The dirtyPrice of the bond is: {dirtyPrice:.2f}")

    npv = bond.NPV()
    print(f"The npv of the bond is: {npv:.2f}")

    for cf in bond.cashflows():
        print("CashFlow: {}, {}".format(cf.date().ISO(), cf.amount()))
    yield_rate = bond.bondYield(cleanPrice,
                                day_count,
                                ql.Continuous,#ql.Compounded,
                                ql.Annual)
    print(f"The yield of the bond is: {yield_rate:.2%}")
    return cleanPrice

def calculate_option(option_request):

    pricing_service = OptionPricingService()

    # when
    price = pricing_service.execute(option_request)
    return price

option_request = EuropeanOptionPriceRequest(issue_date=datetime.now(),
                                                maturity_date=datetime.now() + relativedelta(years=+3),
                                                spot_price=13.0,
                                                strike_price=13.0,
                                                volatility=0.20,
                                                risk_free_rate=0.0198,
                                                dividend_rate=0.015,
                                                option_type=OptionTypeEnum.CALL)


def equation(contract_size, option_price, zero_bond_price, fees):
    return ((zero_bond_price + fees - 100.0) + (contract_size * option_price)) - 100


def solver(option_price, zero_bond_price, fees):
    target = [0]
    root = fsolve(equation, target, args=(option_price, zero_bond_price, fees, ))
    print("Option Contract Size:", root[0])

print('______Begin_________________________________________')
option_price = calculate_option(option_request)
print('option_price: {}'.format(option_price))
zero_bond_price = calculate_zero_bond(option_request)
fees = 1.5
print('zero_bond_price: {}'.format(zero_bond_price))
issue_price = zero_bond_price + fees + option_price.option_price
print('issue_price: {}'.format(issue_price))

solver(option_price.option_price, zero_bond_price, issue_price)
print('______End___________________________________________')