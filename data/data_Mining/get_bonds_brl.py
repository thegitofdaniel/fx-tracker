########################################################
# import packages
import json
import pandas as pd

########################################################
# get data
with open("data/data_Mining/funcParams.json") as file:
    funcParams = json.load(file)
    url = funcParams["brl"]["bonds"]["url"]

df = pd.read_csv(url,sep=";")

########################################################
# process data

# rename columns
df = df.rename(columns={"Tipo Titulo":"bond_type"
                        ,"Data Base": "date"
                        ,"Data Vencimento": "maturity_date"
                        ,"PU Compra Manha": "bid_price"
                        ,"PU Venda Manha": "ask_price"
                        ,"PU Base Manha": "market_price"
                        ,"Taxa Compra Manha": "bid_yield"
                        ,"Taxa Venda Manha": "ask_yield"
                       })

# declare variable format
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
df["maturity_date"] = pd.to_datetime(df["maturity_date"], format="%d/%m/%Y")
    
for i in ["bid_price","ask_price","market_price"]:
    df[i]=pd.to_numeric(df[i].apply(lambda x: x.replace(",",".")))
    
for i in ["bid_yield","ask_yield"]:
    df[i]=pd.to_numeric(df[i].apply(lambda x: x.replace(",",".")))/100

# bond type
dict_bond_types = {"Tesouro IGPM+ com Juros Semestrais":"igpms"
                   ,"Tesouro IPCA+":"ipca"
                   ,"Tesouro IPCA+ com Juros Semestrais":"ipcas"
                   ,"Tesouro Prefixado":"pre"
                   ,"Tesouro Prefixado com Juros Semestrais":"pres"
                   ,"Tesouro Selic":"selic"}

assert set(df.bond_type.unique())==set(dict_bond_types.keys())
df["bond_type"] = df["bond_type"].apply(lambda x: dict_bond_types[x])

# add useful variables
dict_indexed = {"pres": True
                ,"selic": True
                ,"ipca": True
                ,"ipcas": True
                ,"igpms": True
                ,"pre": False}

df["indexed"]=df["bond_type"].apply(lambda x: dict_indexed[x])

dict_pays_coupom = {"pres": True
                    ,"selic": False
                    ,"ipca": False
                    ,"ipcas": True
                    ,"igpms": True
                    ,"pre": False}

df["pays_coupom"]=df["bond_type"].apply(lambda x: dict_pays_coupom[x])

df = df.sort_values(by=["maturity_date","date"])
df = df.reset_index(drop=True)

############################################
# save data as parquet
df.to_parquet("data/bronze/bonds_brl.parquet")
