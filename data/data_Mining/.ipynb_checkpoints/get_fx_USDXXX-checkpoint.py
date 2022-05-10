########################################################
# import packages
import argparse
import json
import pandas as pd
from fredapi import Fred

########################################################
with open("secrets/secrets.json") as file:
    secrets = json.load(file)
    api_key = secrets["fred_api_key"]

parser = argparse.ArgumentParser(description='Get the FX time series for domestic and foreign currency pair.')
parser.add_argument(dest='dom_cur', type=str, help='The domestic currency (e.g. usd, eur, brl, etc).')
parser.add_argument(dest='for_cur', type=str, help='The foreign currency (e.g. usd, eur, brl, etc).')
parser.add_argument(dest='series_code', type=str, help='The FRED API series code.')
args = parser.parse_args()

dom_cur=args.dom_cur
for_cur=args.for_cur
series_code=args.series_code

assert(len(dom_cur)==3)
assert(len(for_cur)==3)

curr_pair = dom_cur+for_cur

########################################################
# get data
fred = Fred(api_key=api_key)
series = fred.get_series(series_code)

########################################################
# process data
    
df = series.dropna()

df = pd.DataFrame(df)

df = df.reset_index()

df = df.rename(columns={"index": "date", 0: "fx_"+curr_pair})

if series_code[-2:]=="US":
    usd_base=True
else:
    usd_base=False

if not usd_base:
    df["fx_"+curr_pair]=1/df["fx_"+curr_pair]

df.date = pd.to_datetime(df.date, format="%Y/%m/%d")

df = df.set_index("date")

########################################################
# save data as parquet
df.to_parquet("data/bronze/fx_"+curr_pair+".parquet")
