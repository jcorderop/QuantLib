#https://quant.stackexchange.com/questions/60776/getting-quarterly-forward-rates-with-quantlib
import QuantLib as ql
import matplotlib.pyplot as plt

terms = ['1', '2', '3', '4', '5', '6', '7', '8',
         '9', '10', '12', '15', '20', '25', '30', '40', '50']
rate = [0.17, 0.17800000000000002, 0.244, 0.364, 0.499,
        0.6409999999999999, 0.773, 0.887, 0.987, 1.074, 1.214, 1.355,
        1.4809999999999999, 1.5390000000000001, 1.567,
        1.527, 1.45]

index = ql.USDLibor(ql.Period('3M'))
helpers = []
dc = ql.Actual360()

for term, r in zip(terms, rate):
    swapIndex = ql.UsdLiborSwapIsdaFixAm(ql.Period(int(term), ql.Years))
    helpers.append(ql.SwapRateHelper(r / 100, swapIndex))

curve = ql.PiecewiseLogCubicDiscount(0, ql.TARGET(), helpers, dc)
curve.enableExtrapolation()

days = ql.MakeSchedule(curve.referenceDate(), curve.maxDate(), ql.Period('3M'))
fwds = [
    curve.forwardRate(d, ql.UnitedStates(ql.UnitedStates.Settlement).advance(d, 90, ql.Days), dc, ql.Simple).rate()
    for d in days
]

print(len(fwds))
print(len(rate))
plt.plot([dt.to_date() for dt in days], fwds, color ='tab:blue')
plt.show()