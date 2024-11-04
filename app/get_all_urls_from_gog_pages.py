import pandas as pd
import tqdm

from bs4 import BeautifulSoup
from datetime import date
from requests import get
from warnings import warn

all_urls = []


requests = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.127 Safari/537.36'}


def get_total_pages():
    # Make a get request
    games = get('https://www.gog.com/en/games',
                headers=headers)

    # Fazendo novas tentativas de request se html vier vazio
    while len(games.text) == 0:
        games = get('https://www.gog.com/en/games',
                    headers=headers)

    # Parse the game response content into the beautiful soup object
    game_soup = BeautifulSoup(games.text, 'html.parser')

    container_div = game_soup.find_all('div', class_='small-pagination')

    container_span = container_div[0].find_all('span')

    page_number = container_span[2].text

    return int(page_number)

try:
    pages = [str(i + 1) for i in range(get_total_pages())]
except Exception as e:
    print(e)

for i in tqdm.tqdm(range(len(pages)), ncols=100, colour="blue", desc="Coleta de páginas"):
    # for i in tqdm.tqdm(range(1, get_total_pages()), ncols=100, colour="blue", desc="Coleta de páginas"):

    # Make a get request
    games = get('https://www.gog.com/en/games?order=asc:storeReleaseDate&page=' + pages[i],
                headers=headers)

    # Fazendo novas tentativas de request se html vier vazio
    while len(games.text) == 0:
        games = get('https://www.gog.com/en/games?order=asc:storeReleaseDate&page=' + pages[i],
                    headers=headers)

    # Show a warning if a non 200 status code is returned
    if games.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, games.status_code))

    # Break the loop if the requests exceed 10
    if requests > 10:
        warn('Number of requests was greater than expected.')
        break

    # Parse the game response content into the beautiful soup object
    game_soup = BeautifulSoup(games.text, 'html.parser')

    # Find the major tag peculiar to each game
    container = game_soup.find_all('a', class_='product-tile product-tile--grid')

    # Iterate through the major tag
    for con in container:
        # Scrape the url
        all_urls.append(con.get('href'))

# Cria um dataframe a partir da lista transformada
urls_dataframe = pd.DataFrame({'url': all_urls})

now = date.today()

dt_string = now.strftime("%Y_%m_%d")

aux_result_all_urls = "dados/result_all_urls_gog_" + dt_string + ".json"

# Transformando os dados da coluna URL em um csv e importando para um arquivo
with open(aux_result_all_urls, 'w') as f:
    f.write(urls_dataframe.to_json())

with open('dados/result_all_urls_gog.json', 'w') as f:
    f.write(urls_dataframe.to_json())
