from datetime import datetime
from functools import reduce
import json
import pandas as pd
import numpy as np
from pandas import json_normalize

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 80)

pk_meta = []
pk_ign = []
pk_gog = []
df = pd.DataFrame()

# def search_all(search_str):
#     print(search(search_str, final_df, False))


def search(regex: str, df, case=False):
    """Search all the text columns of `df`, return rows with any matches."""
    textlikes = df.select_dtypes(include=[object, "string"])
    return df[
        textlikes.apply(
            lambda column: column.str.contains(regex, regex=True, case=case, na=False)
        ).any(axis=1)
    ]


def shift_first_column(df):
    # shift column 'Name' to first position
    first_column = df.pop('PK')

    # insert column using insert(position,column_name,
    # first_column) function
    df.insert(0, 'PK', first_column)


# # Realiza a leitura do arquivo auxiliador
# with open('dados/result_metacritic.json', 'r') as f:
#     search_meta = f.read()
#
# df_meta = pd.read_json(search_meta)
#
# df_meta = df_meta.drop_duplicates(subset=['URL'], keep='last')
#
# del df_meta["index"]
#
# for k, v in df_meta['URL'].items():
#     pk_meta.append(v.split('/')[-2])
#
# df_meta['PK'] = pk_meta
#
# shift_first_column(df_meta)
#
# with open('dados/result_ign.json', 'r') as f:
#     search_ign = f.read()
#
# df_ign = pd.read_json(search_ign)
#
# del df_ign["index"]
#
# for k, v in df_ign['URL'].items():
#     pk_ign.append(v.split('/')[-1])
#
# df_ign['PK'] = pk_ign
#
# shift_first_column(df_ign)
#
# with open('dados/result_gog.json', 'r') as f:
#     search_gog = f.read()
#
# # df_gog = pd.read_json(search_gog, convert_dates=['Scrape_date'])
#
# df_gog = pd.read_json(search_gog)
#
# for k, v in df_gog['URL'].items():
#     pk_gog.append(v.split('/')[-1].replace("_", "-"))
#
# date_gog = []
# # for i in df_gog['Scrape_date'].lenght:
# #     print(df_gog(i))
# #     print(datetime.fromtimestamp(df_gog[i]))
# #     date_gog.append(datetime.utcfromtimestamp(df_gog[i]))
#
# for index, row in df_gog.iterrows():
#     ts = int(row['Scrape_date'])/1000
#     date_gog.append(datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])
#
# df_gog['PK'] = pk_gog
#
# df_gog['Scrape_date'] = date_gog
#
# shift_first_column(df_gog)
#
# df_all = [df_meta, df_ign, df_gog]
#
# final_df = reduce(lambda left, right: pd.merge(left, right, on=['PK'],
#                                                how='outer'), df_all)
#
# string = input("Por favor, informe o termo a ser buscado ou digite 'sair' para encerrar a pesquisa: ")

# while string != 'sair':
#     search_all(string)
#     print()
#     string = input("Por favor, informe o termo a ser buscado ou digite 'sair' para encerrar a pesquisa: ")
