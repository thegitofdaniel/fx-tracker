########################################################
# import packages
import argparse
import json
import pandas as pd
from fredapi import Fred

########################################################

# parse arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument(dest='country', type=str, help='e.g. usd, brl, eur, etc.')
parser.add_argument(dest='series_name', type=str, help='e.g. CPI, interest, etc.')
args = parser.parse_args()

with open("secrets/secrets.json") as file:
    secrets = json.load(file)
    api_key = secrets["fred_api_key"]

observation_start='31/7/2001'

rates = {
        ('01-month','DGS1MO')
        ,('03-month','DGS3MO')
        ,('06-month','DGS6MO')
        ,('01-year','DGS1')
        ,('02-year','DGS2')
        ,('03-year','DGS3')
        ,('05-year','DGS5')
        ,('07-year','DGSS7')
        ,('10-year','DGS10')
        ,('20-year','DGS20')
        ,('30-year','DGS30')
        }


########################################################
# get data

fred = Fred(api_key=api_key)
series = fred.get_series(series_code)
    
########################################################
# process data

df = series.dropna()

df = pd.DataFrame(df)

df = df.reset_index()
df = df.rename(columns={"index": "date", 0: series_name+"_"+country})

df.date = pd.to_datetime(df.date, format="%Y/%m/%d")

df = df.set_index("date")

# adjustements for correct unit
if series_name+"_"+country in ["inflation_f12m_usd"]:
    df[series_name+"_"+country]/=100

########################################################
# save data as parquet
df.to_parquet("data/bronze/"+series_name+"_"+country+".parquet")