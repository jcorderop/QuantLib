import QuantLib as ql

# Option parameters
option_type = ql.Option.Call  # Call or Put
barrier_type = ql.Barrier.UpIn  # Barrier type (e.g., UpIn, UpOut, DownIn, DownOut)
barrier = 100  # Barrier level
strike = 95  # Option strike price
expiry_date = ql.Date(31, 12, 2023)  # Option expiry date
payment_date = ql.Date(31, 12, 2024)  # Option payment date
spot_price = 100  # Underlying asset spot price
volatility = 0.2  # Volatility of the underlying asset
risk_free_rate = 0.05  # Risk-free interest rate
dividend_yield = 0.0  # Dividend yield of the underlying asset

# Option and barrier schedule
#option_schedule = ql.Schedule(expiry_date, expiry_date, ql.Period(ql.Daily))
#barrier_schedule = ql.Schedule(option_schedule)

# Option and barrier payoff
option_payoff = ql.PlainVanillaPayoff(option_type, strike)
#barrier_payoff = ql.CashOrNothingPayoff(barrier_type, barrier, ql.CashOrNothingPayoff.Call, 0.0)
barrier_payoff = ql.BarrierOption()
# Option and barrier exercise
option_exercise = ql.EuropeanExercise(expiry_date)
barrier_exercise = ql.EuropeanExercise(expiry_date)

# Option and barrier instruments
option = ql.VanillaOption(option_payoff, option_exercise)
barrier_option = ql.BarrierOption(barrier_payoff, barrier_exercise)#, barrier_schedule, barrier_exercise)

# Pricing engine
spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
vol_handle = ql.QuoteHandle(ql.SimpleQuote(volatility))
rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(payment_date, risk_free_rate, ql.Actual365Fixed()))
div_yield_handle = ql.YieldTermStructureHandle(ql.FlatForward(payment_date, dividend_yield, ql.Actual365Fixed()))

process = ql.BlackScholesMertonProcess(spot_handle, div_yield_handle, rate_handle, vol_handle)
engine = ql.AnalyticBarrierEngine(process)

# Assign pricing engine to option and barrier option
option.setPricingEngine(engine)
barrier_option.setPricingEngine(engine)

# Calculate option and barrier option prices
option_price = option.NPV()
barrier_option_price = barrier_option.NPV()

print("Option price:", option_price)
print("Barrier option price:", barrier_option_price)