import pandas as pd
import glob, os, json

from datetime import date

json_dir = 'dados/result_metacritic'

json_pattern = os.path.join(json_dir, '*.json')
file_list = glob.glob(json_pattern)

json_data = ""

dfs = []
for file in file_list:
    with open(file) as f:
        json_data = pd.json_normalize(json.loads(f.read()))
        json_data['DIR'] = file.rsplit("/", 1)[-1]
    dfs.append(json_data)
df = pd.concat(dfs)

now = date.today()

dt_string = now.strftime("%Y_%m_%d")

result_meta_file_name = "dados/result_metacritic_" + dt_string + ".json"

df.reset_index(inplace=True)

# Transformando a tabela em um json e importando para um arquivo
with open(result_meta_file_name, 'w') as f:
    f.write(df.to_json(orient='records'))

with open('dados/result_metacritic.json', 'w') as f:
    f.write(df.to_json(orient='records'))

# # # IGN # # #
# Criando uma lista de nomes de jogos
gnames_to_csv = []
for url in df['URL']:
    url = url.replace('---', '-')
    gnames_to_csv.append(url.split('/')[-2])

# Cria um dataframe a partir da lista transformada
gnames_dataframe = pd.DataFrame({'url': gnames_to_csv})

now = date.today()

dt_string = now.strftime("%Y_%m_%d")

aux_ign_file_name = "dados/aux_ign_" + dt_string + ".json"

# Transformando os dados da coluna URL em um csv e importando para um arquivo
with open(aux_ign_file_name, 'w') as f:
    f.write(gnames_dataframe.to_json())

with open('dados/aux_ign.json', 'w') as f:
    f.write(gnames_dataframe.to_json())
