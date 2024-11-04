import pandas as pd
import tqdm
from bs4 import BeautifulSoup
from datetime import date
from requests import get
from warnings import warn

all_urls = []

requests = 0
url_default = 'https://www.metacritic.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.127 Safari/537.36'}


def get_total_pages():
    # Make a get request
    games = get('https://www.metacritic.com/browse/game/all/all/all-time/new/?releaseYearMin=1910&releaseYearMax=2024'
                '&page=1',
                headers=headers)

    # Fazendo novas tentativas de request se html vier vazio
    while len(games.text) == 0:
        games = get('https://www.metacritic.com/browse/game/all/all/all-time/new/?releaseYearMin=1910&releaseYearMax'
                    '=2024&page=1',
                    headers=headers)

    # Parse the game response content into the beautiful soup object
    game_soup = BeautifulSoup(games.text, 'html.parser')

    # Find the major tag peculiar to each game
    container = game_soup.find_all('span',
                                   class_='c-navigationPagination_itemButton u-flexbox u-flexbox-alignCenter '
                                          'u-flexbox-justifyCenter g-text-xsmall g-inner-spacing-left-small '
                                          'g-inner-spacing-right-small g-inner-spacing-top-small '
                                          'g-inner-spacing-bottom-small')

    num_of_games = container[2].text

    nog = "".join([ele for ele in num_of_games if ele.isdigit()])
    nog = int(nog) + 1

    return nog


try:
    pages = [str(i) for i in range(get_total_pages())]
except Exception as e:
    print(e)

for i in tqdm.tqdm(range(1, len(pages)), ncols=100, colour="blue", desc="Coleta de páginas"):

    # Make a get request
    games = get('https://www.metacritic.com/browse/game/all/all/all-time/new/?releaseYearMin=1910&releaseYearMax=2024'
                '&page=' + pages[i],
                headers=headers)

    # Fazendo novas tentativas de request se html vier vazio
    while len(games.text) == 0:
        games = get('https://www.metacritic.com/browse/game/all/all/all-time/new/?releaseYearMin=1910&releaseYearMax'
                    '=2024&page=' + pages[i],
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
    container = game_soup.find_all('a', class_='c-finderProductCard_container g-color-gray80 u-grid')

    # Iterate through the major tag
    for con in container:
        # Scrape the url
        all_urls.append(url_default + con.get('href'))

# Cria um dataframe a partir da lista transformada
urls_dataframe = pd.DataFrame({'url': all_urls})

now = date.today()

dt_string = now.strftime("%Y_%m_%d")

aux_result_all_urls = "dados/result_all_urls_metacritic_" + dt_string + ".json"

# Transformando os dados da coluna URL em um csv e importando para um arquivo
with open(aux_result_all_urls, 'w') as f:
    f.write(urls_dataframe.to_json())

with open('dados/result_all_urls_metacritic.json', 'w') as f:
    f.write(urls_dataframe.to_json())
