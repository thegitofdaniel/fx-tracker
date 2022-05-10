########################################################
# import packages
import json
import pandas as pd
import requests
from requests.auth import HTTPDigestAuth

########################################################

# Bank interest rates - overnight deposits from corporations - euro area
# url = "https://sdw-wsrest.ecb.europa.eu/service/data/MIR/M.U2.B.L21.A.R.A.2240.EUR.N?format=jsondata"

with open("data/data_Mining/funcParams.json") as file:
    funcParams = json.load(file)
    url = funcParams["eur"]["interest"]["url"]
    
# get data
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.content)
    
else:
    print("Failed request")
    print(response.status_code)

########################################################
# process data

# values
observations = data["dataSets"][0]["series"]["0:0:0:0:0:0:0:0:0:0"]["observations"]
observations = [i[0] for i in list(observations.values())]

# dates
dates = data
dates = dates["structure"]["dimensions"]["observation"][0]["values"]
dates = [i["id"] for i in list(dates)]

assert len(dates)==len(observations)

series = [(dates[i],observations[i]) for i in range(len(observations))]

df = pd.DataFrame(series)

df = df.rename(columns={0: "date", 1: "interest_eur"})

df.interest_eur/=100

df.date = pd.to_datetime(df.date, format="%Y/%m")

df = df.set_index("date")

########################################################
# save data as parquet
df.to_parquet("data/bronze/interest_eur.parquet")