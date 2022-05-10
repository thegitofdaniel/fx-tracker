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
    url = funcParams["brl"]["inflation_f12m"]["url"]
    
# get data
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.content)
    
else:
    print("Failed request")
    print(response.status_code)

########################################################
# process data
data = data["value"]

df = pd.DataFrame(data)

df = df.rename(columns={'Indicador': 'metric'
                        , 'Data': 'date'
                        , 'Media': 'surveyMean'
                        , 'Mediana': 'surveyMedian'
                        , 'DesvioPadrao': 'surveyStd'
                        , 'Suavizada': 'adjusted'
                        , 'Minimo': 'surveyMin'
                        , 'Maximo': 'surveyMax'
                        , 'numeroRespondentes': 'nparticipants'
                        ,'baseCalculo': 'base'
                       })

df.surveyMean = pd.to_numeric(df.surveyMean)/100
df.surveyMedian = pd.to_numeric(df.surveyMedian)/100
df.surveyStd = pd.to_numeric(df.surveyStd)/100
df.surveyMin = pd.to_numeric(df.surveyMin)/100
df.surveyMax = pd.to_numeric(df.surveyMax)/100

df.nparticipants = pd.to_numeric(df.nparticipants)
df.base = pd.to_numeric(df.base)

df.date = pd.to_datetime(df.date, format="%Y-%m-%d")

df = df[df["base"]==0]
df["inflation_f12m_brl"]=df["surveyMedian"]

df = df.sort_values(by=["date"], ascending=True)
df = df.set_index("date")

########################################################
# save data as parquet
df.to_parquet("data/bronze/inflation_f12m_brl.parquet")
