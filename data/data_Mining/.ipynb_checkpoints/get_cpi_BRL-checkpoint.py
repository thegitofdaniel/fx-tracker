########################################################
# import packages
import json
import pandas as pd
import requests
from requests.auth import HTTPDigestAuth

########################################################
# get data
# https://sidra.ibge.gov.br/tabela/1737
with open("data/data_Mining/funcParams.json") as file:
    funcParams = json.load(file)
    url = funcParams["brl"]["cpi"]["url"]

df = pd.read_csv(url,sep=";")
print(df.columns)

########################################################
# get data
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.content)
    
else:
    print("Failed request")
    print(response.status_code)
    
########################################################
# process data
df = pd.DataFrame(data[1:])

df = df[["D3N","V"]]

df = df.rename(columns={"D3N": "date", "V": "cpi_brl"})

df.cpi_brl = pd.to_numeric(df.cpi_brl)

conversor = {"janeiro":"01"
            ,"fevereiro":"02"
            ,"março":"03"
            ,"abril":"04"
            ,"maio":"05"
            ,"junho":"06"
            ,"julho":"07"
            ,"agosto":"08"
            ,"setembro":"09"
            ,"outubro":"10"
            ,"novembro":"11"
            ,"dezembro":"12"}

df.date = df.date.apply(lambda date: "01/"+conversor[date[:-5]]+"/"+date[-4:])

df.date = pd.to_datetime(df.date, format="%d/%m/%Y")

df = df.set_index("date")

########################################################
# save data as parquet
df.to_parquet("data/bronze/cpi_brl.parquet")
