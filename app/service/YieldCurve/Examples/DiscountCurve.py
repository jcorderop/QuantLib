#https://quant.stackexchange.com/questions/51366/quantlib-interpolateddiscountcurve-zero-forward-rate-at-endpoint
import pandas as pd
import QuantLib as ql
import matplotlib.pyplot as plt

dates =  [
    '2020-02-26',  '2020-02-27',  '2020-02-28',  '2020-03-10',  '2020-03-17',  '2020-04-01',  '2020-04-30',  '2020-06-01',  '2020-07-01',  '2020-07-30',  '2020-09-01',
    '2020-09-30',  '2020-10-30',  '2020-12-01',  '2020-12-30',  '2021-02-01',  '2021-03-01',  '2021-09-01',  '2022-03-01',  '2022-08-31',  '2023-03-01',  '2024-03-01',
    '2025-03-01',  '2026-03-01',  '2027-03-01',  '2028-03-01',  '2029-03-01',  '2030-03-01',  '2031-03-01',  '2032-03-01',  '2035-03-01',  '2040-03-01',  '2045-03-01',
    '2050-03-01']

dfs = [1,  1.0000102501050636,  1.000020500315192,  1.000135036504439,  1.0002140481753308,  1.0003903064472135,  1.0007383708059454,  1.0011864659905814,  1.001606452340883,
 1.0020206702099752,  1.0025224673306343,  1.0030070050312758,  1.0034783631568704,  1.0040034616057292,  1.0045093968882473,  1.0050604130179728,  1.0055474482943991,
 1.0087481016987652, 1.01191304422858, 1.0148211625629888, 1.0174479377825414, 1.0215623647797287, 1.023909696966405, 1.0242610376714252, 1.02262864674708, 1.0191710493588495,
 1.013740853380904, 1.0061949692591952, 0.9981081305430491, 0.9884922702699313, 0.9614484818437421, 0.913861136055078, 0.8771539172898629, 0.8489994312646763]

qlDates = [ql.Date(dt, '%Y-%m-%d') for dt in dates]

params = [qlDates, dfs, ql.Actual365Fixed(),ql.UnitedStates(ql.UnitedStates.Settlement)]
curves = {
    'DiscountCurve': ql.DiscountCurve(*params),
    'NaturalCubicDiscountCurve': ql.NaturalCubicDiscountCurve(*params),
    'MonotonicLogCubicDiscountCurve': ql.MonotonicLogCubicDiscountCurve(*params)
}
plt.figure(figsize=(10,5))
for key in curves:
    crv = curves[key]
    crv.enableExtrapolation()
    times = crv.times()
    zeros = [crv.zeroRate(date, ql.Actual365Fixed(), ql.Continuous).rate() for date in crv.dates()]
    plt.plot(times, zeros, label=f"Spot {key}")
    fwds = [crv.forwardRate(date, date + ql.Period('1d'), ql.Actual360(), ql.Simple).rate() for date in crv.dates()]
    plt.plot(times, fwds, label=f"Fwd {key}")

plt.legend()