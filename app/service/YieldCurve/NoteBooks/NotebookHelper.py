import json
from datetime import datetime

import QuantLib as ql
import pandas as pd
from IPython.core.display_functions import display


def get_tenor(tenor: str) -> ql.Period:
    tenor_split = tenor.split(' ')
    period = None
    tenor_value = int(tenor_split[0])
    if tenor_split[1] == 'day':
        period = ql.Period(tenor_value, ql.Days)
    if tenor_split[1] == 'week':
        period = ql.Period(tenor_value, ql.Weeks)
    elif tenor_split[1] == 'month':
        period = ql.Period(tenor_value, ql.Months)
    elif tenor_split[1] == 'year':
        period = ql.Period(tenor_value, ql.Years)
    return period


def convert_tenor(tenor):
    if '1BD' in tenor:
        new_tenor = '0 day'
    elif 'W' in tenor:
        new_tenor = tenor.replace('W', ' week')
    elif 'M' in tenor:
        new_tenor = tenor.replace('M', ' month')
    elif 'Y' in tenor:
        new_tenor = tenor.replace('Y', ' year')
    return new_tenor


def calculate_base_points(methods_curves, df_index_tenors):
    for curve in methods_curves:
        dfs = [methods_curves[curve].discount(idx) for idx in df_index_tenors.index]
        df_index_tenors[curve] = dfs


def build_points(swaps):
    benchmark_points = []
    for swap in swaps:
        tenor = convert_tenor(swap[0])
        rate = swap[1]
        point = {
            "tenor": tenor,
            "rate": rate
        }
        benchmark_points.append(point)
    tenor_points = {'benchmark_points': benchmark_points}
    print(tenor_points)
    return tenor_points


def plot_forward_rates(curve_dates, methods_curves, settings, index_curve_name, df_raw_yields, compounding_type=ql.Simple):
    #https://stackoverflow.com/questions/74437250/how-does-quantlib-forwardrate-function-work
    data_forward_rates = []
    benchmark_rate = []
    benchmark_date = []

    ref_date = list(methods_curves.values())[0].referenceDate()
    count = 0
    rate = None
    for date in curve_dates:
        list_rate = []
        for curve in methods_curves:
            curve = methods_curves[curve]
            curve_rates = curve.forwardRate(ref_date,
                                      date,
                                      curve.dayCounter(),
                                      compounding_type).rate()

            list_rate.append(curve_rates)

        if date >= df_raw_yields['Yield'].index[count]:
            rate = df_raw_yields['Yield'].iloc[count]
            benchmark_rate.append([rate] + list_rate)
            benchmark_date.append(date)
            count += 1

        data_forward_rates.append(list_rate+[rate])
    df_forward_rate = pd.DataFrame(data=data_forward_rates, columns=list(index_curve_name)+['yield Source'], index=curve_dates)
    df_forward_rate.plot(linestyle='-', markevery=500, figsize=(15, 5), ylabel='Forward Rate', xlabel='Period', grid=True, title='Forward Curves')

    df = pd.DataFrame(data=benchmark_rate, columns=['yield Source']+list(index_curve_name), index=benchmark_date)
    display(df)


def plot_zero_rates(curve_dates, methods_curves, settings, index_curve_name, df_raw_yields, compounding_type=ql.Continuous, frequency=ql.Annual):
    data_zero_rates = []
    benchmark_rate = []
    benchmark_date = []

    count = 0
    rate = None
    for date in curve_dates:
        list_rate = []
        for curve in methods_curves:
            rates = methods_curves[curve].zeroRate(date,
                                                   settings.day_counter,
                                                   compounding_type,
                                                   frequency).rate()
            list_rate.append(rates)
        try:
            if date >= df_raw_yields['Yield'].index[count]:
                rate = df_raw_yields['Yield'].iloc[count]
                benchmark_rate.append([rate] + list_rate)
                benchmark_date.append(date)
                count += 1
        except:
            pass
        data_zero_rates.append(list_rate+[rate])

    df_jumps = pd.DataFrame(data=data_zero_rates, columns=list(index_curve_name)+['yield'], index=curve_dates)
    df_jumps.plot(linestyle='-', markevery=500, figsize=(15, 5), ylabel='Zero Rate', xlabel='Period', grid=True,
                  title='Zero Curves')

    df = pd.DataFrame(data=benchmark_rate, columns=['yield Source']+list(index_curve_name), index=benchmark_date)
    display(df)


def plot_discount(curve_dates, methods_curves, settings, index_curve_name):
    data_discount = []

    for date in curve_dates:
        list_rate = []
        for curve in methods_curves:
            rates = methods_curves[curve].discount(date)
            list_rate.append(rates)
        data_discount.append(list_rate)

    df_discount = pd.DataFrame(data=data_discount, columns=index_curve_name, index=curve_dates)
    df_discount.plot(linestyle='-', markevery=500, figsize=(15, 5), ylabel='Discount', xlabel='Period', grid=True,
                     title='Discount Curves')


def print_cash_flows_fixed_bond(bond):
    fields = [
    'accrualDays', 'accrualEndDate', 'accrualPeriod', 'accrualStartDate',
    'amount',  'date', 'dayCounter', 'interestRate', 'nominal',  'rate'
    ]

    data = []
    for cf in list(map(ql.as_fixed_rate_coupon, bond.cashflows()))[:-1]:
        data.append({fld: getattr(cf, f'{fld}')() for fld in fields})
    df = pd.DataFrame.from_dict(data, orient='columns')
    display(df)


def print_cash_flows_zero_bond(bond):
    for cf in bond.cashflows():
        print(f'date: {cf.date()}')
        print(f'amount: {cf.amount()}')
        print(f'hasOccurred: {cf.hasOccurred()}')
        print(f'thisown: {cf.thisown}')


def print_bond_pricing(curve, bond, settings):
    coupon_yield = bond.bondYield(settings.day_counter,
                                  settings.compounding,
                                  settings.compounding_frequency)

    data = {'Curve': curve,
        'CleanPrice': bond.cleanPrice(),
        'DirtyPrice': bond.dirtyPrice(),
        'AccruedAmt': bond.accruedAmount(),
        'Yield': coupon_yield,
        'NPV': bond.NPV()
        }
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Value'])
    display(df)


def calculate_bond_from_yield_curve(methods_curves, bond, settings):
    for curve in methods_curves:
        discounting_term_structure = ql.RelinkableYieldTermStructureHandle()
        discounting_term_structure.linkTo(methods_curves[curve])
        discounting_engine = ql.DiscountingBondEngine(discounting_term_structure)
        bond.setPricingEngine(discounting_engine)
        print('=' * 100)
        print_bond_pricing(curve, bond, settings)
        print_cash_flows_zero_bond(bond)


def calculate_bond_from_rate(methods_curves, bond, settings, start_date, end_date, frequency=ql.Annual):
    for curve in methods_curves:
        # discounting_term_structure = ql.RelinkableYieldTermStructureHandle()

        interest_rate = methods_curves[curve].forwardRate(start_date,
                                                          end_date,
                                                          settings.day_counter,
                                                          ql.Simple).rate()
        interest_rate = methods_curves[curve].zeroRate(end_date,
                                                       settings.day_counter,
                                                        ql.Continuous,
                                                       frequency).rate()

        flat_forward = ql.FlatForward(start_date,
                                      interest_rate,
                                      settings.day_counter,
                                      settings.compounding,
                                      settings.compounding_frequency)
        spot_curve_handle = ql.YieldTermStructureHandle(flat_forward)
        # discounting_term_structure.linkTo(spot_curve_handle)
        discounting_engine = ql.DiscountingBondEngine(spot_curve_handle)
        bond.setPricingEngine(discounting_engine)
        print('-' * 50)
        print(f'Rate       : {interest_rate}')
        print_bond_pricing(curve, bond, settings)
        print_cash_flows_zero_bond(bond)


class Settings:
    __today_dt = datetime.now().date()
    today = ql.Date(__today_dt.day, __today_dt.month, __today_dt.year)

    target_day = today + 95
    compounding_frequency = ql.Annual

    fixing_days = 0
    calendar = ql.Switzerland()  # TODO, review what actually Swiss calendar does
    convention = ql.ModifiedFollowing
    end_of_month = False
    day_counter = ql.Actual360()
    compounding_type = ql.Simple
    fixed_frequency = ql.Annual

    settlement_days = 2

    index = ql.Sofr()

#FinMechanics
sofr_swaps = [
    ('1BD',0.050694339),
    ('1W',0.051482818),
    ('2W',0.050516581),
    ('1M',0.050693418),
    ('2M',0.051183173),
    ('3M',0.052179246),
    ('4M',0.053034023),
    ('5M',0.053390716),
    ('6M',0.052693244),
    ('7M',0.052695327),
    ('8M',0.052394946),
    ('9M',0.051137664),
    ('10M',0.054207728),
    ('11M',0.05471223),
    ('12M',0.058945942),
    #('2Y',0.176529845)
]

#FinMechanics discounted
sofr_swaps_discounted = [
    ('1BD',0.999991667),
    ('1W',0.999987306),
    ('2W',0.999977856),
    ('1M',0.999954169),
    ('2M',0.999911660),
    ('3M',0.999867059),
    ('4M',0.999819846),
    ('5M',0.999773298),
    ('6M',0.99973584),
    ('7M',0.999689651),
    ('8M',0.999649805),
    ('9M',0.999614790),
    ('10M',0.999544165),
    ('11M',0.999496474),
    ('12M',0.999402644),
    #('2Y',0.176529845)
]

# https://www.ustreasuryyieldcurve.com/
# 06/06/2023
sofr_swaps_ = [
    #('1BD',0.050694339),
    #('1W',0.051482818),
    #('2W',0.050516581),
    ('1M',0.0525),
    ('2M',0.0535),
    ('3M',0.0546),
    ('4M',0.0547),
    #('5M',0.0546),
    ('6M',0.0546),
    #('7M',0.052695327),
    #('8M',0.052394946),
    #('9M',0.051137664),
    #('10M',0.054207728),
    #('11M',0.05471223),
    ('1Y',0.0517),
    ('2Y',0.0446),
    ('3Y',0.041),
    ('5Y',0.0382),
    ('7Y',0.0377),
    ('10Y',0.0369),
    ('20Y',0.0403),
    ('30Y',0.0389),

    #('2Y',0.176529845)
]


swiss_bonds = {
  "benchmark_points": [
    {
      "tenor": "0 day",
      "rate": 0.015
    },
    {
      "tenor": "1 month",
      "rate": 0.0134
    },
    {
      "tenor": "2 month",
      "rate": 0.0145
    },
    {
      "tenor": "3 month",
      "rate": 0.0146
    },
    {
      "tenor": "6 month",
      "rate": 0.0158
    },
    {
      "tenor": "1 year",
      "rate": 0.0177
    },
    {
      "tenor": "2 year",
      "rate": 0.01068
    },
    {
      "tenor": "3 year",
      "rate": 0.00951
    },
    {
      "tenor": "4 year",
      "rate": 0.00798
    },
    {
      "tenor": "5 year",
      "rate": 0.00806
    },
    {
      "tenor": "6 year",
      "rate": 0.008
    },
    {
      "tenor": "7 year",
      "rate": 0.00802
    },
    {
      "tenor": "8 year",
      "rate": 0.00811
    },
    {
      "tenor": "9 year",
      "rate": 0.0084
    },
    {
      "tenor": "10 year",
      "rate": 0.00853
    }
  ]
}