########################################################
# import packages
import json
import pandas as pd
import requests
from requests.auth import HTTPDigestAuth

########################################################
# get data
# HICP - Overall index
# Euro area (changing composition) - HICP - Overall index, Annual rate of change, Eurostat, Neither seasonally nor working day adjusted
# https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=122.ICP.M.U2.N.000000.4.ANR
# url = "https://sdw-wsrest.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.INX?format=jsondata"

with open("data/data_Mining/funcParams.json") as file:
    funcParams = json.load(file)
    url = funcParams["eur"]["cpi"]["url"]

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.content)
    
else:
    print("Failed request")
    print(response.status_code)
    
########################################################
# process data
# values
observations = data["dataSets"][0]["series"]["0:0:0:0:0:0"]["observations"]
observations = [i[0] for i in list(observations.values())]

# dates
dates = data
dates = dates["structure"]["dimensions"]["observation"][0]["values"]
dates = [i["id"] for i in list(dates)]

assert len(dates)==len(observations)

series = [(dates[i],observations[i]) for i in range(len(observations))]

df = pd.DataFrame(series)

df = df.rename(columns={0: "date", 1: "cpi_eur"})

df.cpi_eur/=100

df.date = pd.to_datetime(df.date, format="%Y/%m")

df = df.set_index("date")

########################################################
# save data as parquet
df.to_parquet("data/bronze/cpi_eur.parquet")
