#########################################
######## First Time #####################
#########################################

cd C:\Users\drr19\OneDrive\CodeRepo\fxfxfx

conda env create -f envs/env_mining.yaml

#########################################
######## Every Time #####################
#########################################

# activate environment
cd C:\Users\drr19\OneDrive\CodeRepo\fxfxfx
conda activate env_mining

##### bronze ############################

# fx pairs
python data\data_Mining\get_fx_USDXXX.py usd brl DEXBZUS
python data\data_Mining\get_fx_USDXXX.py usd eur DEXUSEU

# usd
python data\data_Mining\get_fred_series.py usd cpi
python data\data_Mining\get_fred_series.py usd interest
python data\data_Mining\get_fred_series.py usd inflation_f12m

# brl
python data\data_Mining\get_interest_BRL.py
python data\data_Mining\get_cpi_BRL.py
python data\data_Mining\get_inflation_f12m_BRL.py
python data\data_Mining\get_bonds_BRL.py

# eur
python data\data_Mining\get_interest_EUR.py
python data\data_Mining\get_cpi_EUR.py

##### silver ############################

# brazilian bonds
python data\data_Enriching\b2s_bonds_brl.py

# macro-variables
python data\data_Enriching\b2s_macro.py usd
python data\data_Enriching\b2s_macro.py brl

##### gold ##############################

# macro-variables pairs
python data\data_Enriching\s2g_macro.py usd brl