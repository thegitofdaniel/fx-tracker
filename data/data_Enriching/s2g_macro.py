"""
This file creates a gold table that consolidates monthly values for two countries macroeconomic indicators.

It will add:
- Real FX rates
- Forward yield
"""

import argparse
import pandas as pd
from pandas.tseries.offsets import MonthEnd, MonthBegin

parser = argparse.ArgumentParser(description='Create a silver table.')
parser.add_argument(dest='dom_cur', type=str, help='The domestic currency (e.g. usd, eur, brl, etc).')
parser.add_argument(dest='for_cur', type=str, help='The foreign currency (e.g. usd, eur, brl, etc).')

args = parser.parse_args()

dom_cur=args.dom_cur
for_cur=args.for_cur

assert(len(for_cur)==3)
assert(len(dom_cur)==3)

##################################################

# merge the two dataframes
df_dom = pd.read_parquet("data/silver/macro_"+dom_cur+".parquet")  
df_for = pd.read_parquet("data/silver/macro_"+for_cur+".parquet")  
df = pd.merge(df_dom, df_for, left_index=True, right_index=True, how="outer")

# last adjustements -> we don't want a sparse matrix
max_min_date = max(df_dom.index.min(),df_for.index.min())
df = df[df.index>=max_min_date]

##################################################

# add real exchange rate
if dom_cur == "usd" or for_cur =="usd":
    df = df.drop(columns=["fx_usdusd"])
else:
    # triangulation
    df["fx_"+dom_cur+for_cur]==df["fx_usd"+for_cur]/df["fx_usd"+dom_cur]
    df = df.drop(columns=["fx_usd"+dom_cur])
    df = df.drop(columns=["fx_usd"+for_cur])
    
# get the real exchange rate
i = df.index.max()
fx_deflator = (df["cpi_"+dom_cur]/df.loc[i]["cpi_"+dom_cur])/(df["cpi_"+for_cur]/df.loc[i]["cpi_"+for_cur])
df["fxreal_"+dom_cur+for_cur] = df["fx_"+dom_cur+for_cur]*fx_deflator

# add the inverse exchange rate
df["fx_"+for_cur+dom_cur] = 1 / df["fx_"+dom_cur+for_cur]
df["fxreal_"+for_cur+dom_cur] = 1 / df["fxreal_"+dom_cur+for_cur]

# add the forward yield
df["yield_f12m_"+dom_cur]=df["interest_"+dom_cur]-df["inflation_f12m_"+dom_cur]
df["yield_f12m_"+for_cur]=df["interest_"+for_cur]-df["inflation_f12m_"+for_cur]

##################################################

# save as parquet
filename = "data/gold/macro_"+dom_cur+for_cur+".parquet"
df.to_parquet(filename)