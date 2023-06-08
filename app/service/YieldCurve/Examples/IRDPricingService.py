import QuantLib as ql

# Set up the bond parameters

face_value = 1000
interest_rate = 0.1
maturity_date = ql.Date(9, 3, 2028) # Maturity in 5 years
issue_date = ql.Date(9, 3, 2023) # Issue date today


ql.Settings.instance().evaluationDate = ql.Date(9, 3, 2023)
# Create a bond object

bond = ql.ZeroCouponBond(0, ql.NullCalendar(), face_value, maturity_date)

# Set up the bond engine

#qflatforw = ql.FlatForward(issue_date, interest_rate, ql.ActualActual(ql.ActualActual.ISMA), ql.Compounded, ql.Annual)

qflatforw = ql.FlatForward(issue_date, interest_rate, ql.Actual360(), ql.Compounded, ql.Annual)

spot_curve_handle = ql.YieldTermStructureHandle(qflatforw)
bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
# Assign the bond engine to the bond object

bond.setPricingEngine(bond_engine)

# Calculate the bond price

clean_price = bond.cleanPrice()

print(f"The clean_price of the bond is: {clean_price:.2f}")
dirty_price = bond.dirtyPrice()
print(f"The dirty_price of the bond is: {dirty_price:.2f}")
npv = bond.NPV()
print(f"The npv of the bond is: {npv:.2f}")