########################################################
# parse arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument(dest='dom_cur', type=str, help='The SIDRA url.')
args = parser.parse_args()

url=args.url


########################################################
# get data
# https://sidra.ibge.gov.br/tabela/1737
with open("data/data_Mining/funcParams.json") as file:
    funcParams = json.load(file)
    url = funcParams["cpi_brl_url"]

df = pd.read_csv(url,sep=";")
print(df.columns)