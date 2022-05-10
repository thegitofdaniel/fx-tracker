"""
This file creates a silver table with the most relevant columns related to Brazilian bonds.

The input of this process is the data/bronze/bonds_brl.parquet table.

The output silver table will have:
- The bond type (e.g. NTN-B, LTN, etc);
- The bond maturity date;
- The bond yield, represented by the bid yield (i.e. how much is market willing to pay for it).

Furthermore, it will be enriched with:
- Inflation
- Real Return (i.e. yield - inflation).

The goal of the output silver table is to study the historical performance of Brazilian Bonds, especially which bond type has performed better over the years.
"""

# import packages
import pandas as pd
from pandas.tseries.offsets import MonthEnd, MonthBegin

# read data
df = pd.read_parquet("data/bronze/bonds_brl.parquet")

# filter first rate of the month
df = df[df.date==df.date+MonthBegin(0)]

# change index
df.index = df["date"]

# filter relevant columns
df=df[["bond_type","maturity_date","bid_yield"]]

# annualized rates -> monthly rates
df["bid_yield"]=(1+df["bid_yield"])**(1/12)-1

# add inflation
df_cpi = pd.read_parquet("data/bronze/cpi_brl.parquet")
df_cpi["inflation_brl"]=df_cpi["cpi_brl"]/df_cpi["cpi_brl"].shift(1)-1
df = pd.merge(df,df_cpi["inflation_brl"],how="left",left_index=True,right_index=True)

df["real_return"]=(1+df["bid_yield"])/(1+df["inflation_brl"])-1

df = df.dropna()

filename = "data/silver/bonds_brl.parquet"

df.to_parquet(filename)