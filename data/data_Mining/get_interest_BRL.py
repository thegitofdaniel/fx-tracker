########################################################
# import packages
import json
import pandas as pd
import requests
from requests.auth import HTTPDigestAuth

########################################################
# https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic/resource/b73edc07-bbac-430c-a2cb-b1639e605fa8
# url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json"
with open("data/data_Mining/funcParams.json") as file:
    funcParams = json.load(file)
    url = funcParams["brl"]["interest"]["url"]
    
# get data
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.content)
    
else:
    print("Failed request")
    print(response.status_code)

########################################################
# process data
df = pd.DataFrame(data)

df.valor = pd.to_numeric(df.valor)

df = df.rename(columns={"data": "date", "valor": "interest_brl"})

df.date = pd.to_datetime(df.date, format="%d/%m/%Y")

df.interest_brl = df.interest_brl.apply(lambda interest_brl: ((interest_brl/100)+1)**252-1)

df = df.set_index("date")

########################################################
# save data as parquet
df.to_parquet("data/bronze/interest_brl.parquet")
