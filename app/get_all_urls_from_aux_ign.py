import json
import pandas as pd

from datetime import date

# Realiza a leitura do arquivo auxiliador
with open('dados/aux_ign.json', 'r') as f:
    search = f.read()

# Normaliza o dado para um json
search = json.loads(search)

seen = []
new_dict = {}


# Remove jogos duplicados
for k, v in search['url'].items():
    if v not in seen:
        seen.append(v)
        new_dict[k] = v
    else:
        print(v)

 # Cria um dataframe a partir da lista transformada
    urls_dataframe = pd.DataFrame({'url': new_dict})

    now = date.today()

    dt_string = now.strftime("%Y_%m_%d")

    aux_result_all_urls = "dados/result_all_urls_ign_" + dt_string + ".json"

    # Transformando os dados da coluna URL em um csv e importando para um arquivo
    with open(aux_result_all_urls, 'w') as f:
        f.write(urls_dataframe.to_json())

    with open('dados/result_all_urls_ign.json', 'w') as f:
        f.write(urls_dataframe.to_json())
