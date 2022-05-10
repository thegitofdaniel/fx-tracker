"""
This file creates a silver table that consolidates monthly values for a country's macroeconomic indicators.

The input of this process are:
- interest_xxx
- fx_usdxxx
- cpi_xxx
- inflation_f12m_xxx


The output silver table will have all the above metrics:
- interest_xxx
- fx_usdxxx
- cpi_xxx
- inflation_xxx
- inflation_f12m_xxx

A few details:
- By convention, the values chosen will be EOM;
- However, the date representing each month will be the 1st to ease data manipulation.
"""

import argparse
import pandas as pd
from pandas.tseries.offsets import MonthEnd, MonthBegin

parser = argparse.ArgumentParser(description='Create a silver table.')
parser.add_argument(dest='curr', type=str, help='The domestic currency (e.g. usd, eur, brl, etc).')
args = parser.parse_args()

curr=args.curr

assert(len(curr)==3)

##################################################

# create a dataframe
df = pd.DataFrame()
max_min_date = pd.to_datetime("01/01/1900")

# add the interest rate
df_new = pd.read_parquet("data/bronze/interest_"+curr+".parquet")  
df = pd.merge(df, df_new, left_index=True, right_index=True, how="outer")
max_min_date = max(df_new.index.min(),max_min_date)

# add the exchange rate
if curr == "usd":
    df["fx_usd"+curr] = pd.Series([1 for d in range(len(df.index))]).values
else:
    df_new = pd.read_parquet("data/bronze/fx_usd"+curr+".parquet")
    df_new = df_new["fx_usd"+curr]
    df = pd.merge(df, df_new, left_index=True, right_index=True, how="outer")

max_min_date = max(df_new.index.min(),max_min_date)

# add inflation expectations
df_new = pd.read_parquet("data/bronze/inflation_f12m_"+curr+".parquet")
df_new = df_new["inflation_f12m_"+curr]
df = pd.merge(df, df_new, left_index=True, right_index=True, how="outer")
max_min_date = max(df_new.index.min(),max_min_date)

#########################
# adjustements for both interest and fx
# create rows for ALL days of the year
df = df.reindex(pd.date_range(df.index.min(), df.index.max()))
# interpolate FORWARD
df = df.ffill()
# filter the EOM values
df = df[(df.index==df.index+MonthEnd(0))]
# for convenience, reindex to the FIRST DAY of the month
df.index = df.index+MonthBegin(-1)
#########################

# add cpi, inflation
df_new = pd.read_parquet("data/bronze/cpi_"+curr+".parquet")
df_new["inflation_mom_"+curr] = df_new["cpi_"+curr] / df_new["cpi_"+curr].shift(1) - 1
df_new["inflation_yoy_"+curr] = df_new["cpi_"+curr] / df_new["cpi_"+curr].shift(12) - 1
df = pd.merge(df, df_new, left_index=True, right_index=True, how="outer")
max_min_date = max(df_new.index.min(),max_min_date)

# last adjustements -> we don't want a sparse matrix
df = df[df.index>=max_min_date]

##################################################
# save as parquet
filename = "data/silver/macro_"+curr+".parquet"
df.to_parquet(filename)