cpi
- Consumer Price Index
- The values have no intrinsic meaning; rather, it's the ratio of values contained in different months (i.e. inflation) that matters.
- It should be understood as the price index of an economy at a month's END (EOM).

fx
- Foreign Exchange Rate
- It's the value of buying a foreign currency with your own domestic currency.
- The notation USDEUR 1.14 means that 1 American dollar can buy 1.14 euros.
- FX data comes from FRED, the dollar is always in each pair (though sometimes as domestic and sometimes as foreign currency). FX between two non-USD currencies is done via triangulation.
- It should be understood as the FX at a month's END (EOM).

interest
- Short Term Interest Rate (Policy Rate)
- It's the economy's short term interest rate, used by the local Central Bank as policy rate.
- This rate is given annualized and in decimal (e.g. entry 0.08 corresponds to 8.0% per year).
- The frequency of this series is not the same for all economies:
-- daily: usd, brl
-- monthly: eur -> not very good

inflation_f12m
- The inflation market participants forecast/expect for the next 12 months.
- eur -> missing