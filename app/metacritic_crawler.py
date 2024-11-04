import json
import numpy as np
import pandas as pd
import tqdm

from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from requests import get
from time import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.127 Safari/537.36'}

# all_urls = []
names = []
meta_scores = []
user_scores = []
platforms = []
release_dates = []
developers = []
publishers = []
genres = []
summaries = []
ratings = []
url = []
scrape_date = []

file_page_number = 1

start_time = time()
requests = 0


def salva_parte_do_json(names_aux, meta_scores_aux, user_scores_aux, platforms_aux, release_dates_aux, developers_aux,
                        publishers_aux, genres_aux, summaries_aux, ratings_aux, urls_aux, scrape_date_aux):
    game_df = pd.DataFrame({'Game_name': names_aux,
                            'Meta_score': meta_scores_aux,
                            'User_score': user_scores_aux,
                            'Platforms': platforms_aux,
                            'Release_date': release_dates_aux,
                            'Developer': developers_aux,
                            'Publisher': publishers_aux,
                            'Genres': genres_aux,
                            'Summary': summaries_aux,
                            'Rating': ratings_aux,
                            'URL': urls_aux,
                            'Scrape_date': scrape_date_aux})

    # Opção para preencher os valores NaN
    game_df = game_df.fillna(value=np.nan)

    now = date.today()

    dt_string = now.strftime("%Y_%m_%d")

    file_page_number_format = "{:04d}".format(file_page_number)

    result_meta_file_name = ("dados/result_metacritic/result_metacritic_" + dt_string + "_" + file_page_number_format +
                             ".json")

    # Transformando a tabela em um json e importando para um arquivo
    with open(result_meta_file_name, 'w') as f:
        f.write(game_df.to_json(orient='records', date_format='iso'))

    clean_lists()


def clean_lists():
    names.clear()
    meta_scores.clear()
    user_scores.clear()
    platforms.clear()
    release_dates.clear()
    developers.clear()
    publishers.clear()
    genres.clear()
    summaries.clear()
    ratings.clear()
    url.clear()
    scrape_date.clear()


def remove_urls_from_json(all_urls_list_aux):
    urls_dataframe = pd.DataFrame({'url': all_urls_list_aux})
    with open('dados/result_all_urls_metacritic.json', 'w') as f:
        f.write(urls_dataframe.to_json())


def define_meta_or_user(bs, score_type):
    if score_type == 0:
        for i in range(len(bs)):
            if "." not in bs[i].text:
                return get_meta_score_color(bs[i])
    elif score_type == 1:
        for i in range(len(bs)):
            if "." in bs[i].text:
                return get_user_score_color(bs[i])


def get_meta_score_color(bs):
    score_colors = [bs.find(class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter '
                                   'g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_medium'),
                    bs.find(class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter '
                                   'g-text-bold c-siteReviewScore_yellow g-color-gray90 c-siteReviewScore_medium'),
                    bs.find(class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter '
                                   'g-text-bold c-siteReviewScore_red g-color-white c-siteReviewScore_medium')]

    for sc in range(len(score_colors)):
        if score_colors[sc] is not None:
            return score_colors[sc].text


def get_user_score_color(bs):
    score_colors = [bs.find(class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter '
                                   'g-text-bold c-siteReviewScore_green c-siteReviewScore_user g-color-gray90 '
                                   'c-siteReviewScore_medium'),
                    bs.find(class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter '
                                   'g-text-bold c-siteReviewScore_yellow c-siteReviewScore_user g-color-gray90 '
                                   'c-siteReviewScore_medium'),
                    bs.find(class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter '
                                   'g-text-bold c-siteReviewScore_red c-siteReviewScore_user g-color-white '
                                   'c-siteReviewScore_medium')]

    for sc in range(len(score_colors)):
        if score_colors[sc] is not None:
            return score_colors[sc].text


# Realiza a leitura do arquivo auxiliador
with open('dados/result_all_urls_metacritic.json', 'r') as f:
    search = f.read()

# Normaliza o dado para um json
search = json.loads(search)

all_urls_list = []

for k, v in search['url'].items():
    all_urls_list.append(v)

all_urls_list_aux = all_urls_list[:]

for j in tqdm.tqdm(range(len(all_urls_list)), ncols=100, colour="green", desc="Coleta de dados individuais"):

    webpage = get(all_urls_list[j], headers=headers)

    # Fazendo requisição até retornar o html
    while len(webpage.text) == 0:
        webpage = get(all_urls_list[j], headers=headers)

    bs = BeautifulSoup(webpage.text, 'html.parser')

    gn = ""
    try:
        game_name = bs.find('div',
                            {'class': 'c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium'})
        gn = game_name.text.replace("\n", "").strip()
    except Exception as e:
        gn = np.nan
    names.append(gn)

    gms = []
    game_meta_score = bs.find_all(class_='c-productScoreInfo_scoreNumber u-float-right')
    try:
        gms = define_meta_or_user(game_meta_score, 0) if game_meta_score is not None else np.nan
    except Exception as e:
        gms = np.nan
    meta_scores.append(gms)

    gus = []
    game_user_score = bs.find_all(class_='c-productScoreInfo_scoreNumber u-float-right')
    try:
        gus = define_meta_or_user(game_user_score, 1) if game_meta_score is not None else np.nan
    except Exception as e:
        gus = np.nan
    user_scores.append(gus)

    gpl = []
    try:
        game_initial_release_date = bs.find_all('ul', {'class': 'g-outer-spacing-left-medium-fluid'})[
            0] if bs is not None else np.nan

        gpl_list = game_initial_release_date.find_all('li',
                                                      {'class': 'c-gameDetails_listItem g-color-gray70 u-inline-block'})

        for i in range(len(gpl_list)):
            gp_treated = gpl_list[i].text.replace("\n", "").strip()
            gpl.append(gp_treated)

    except Exception as e:
        gpl = np.nan
    platforms.append(gpl)

    girdl = []
    try:
        game_initial_release_date = \
            bs.find_all('span', {'class': 'g-outer-spacing-left-medium-fluid g-color-gray70 u-block'})[
                0] if bs is not None else np.nan

        girdl = game_initial_release_date.text
    except Exception as e:
        girdl = np.nan
    release_dates.append(girdl)

    gdl = []
    try:
        game_developers_list = bs.find_all('ul', {'class': 'g-outer-spacing-left-medium-fluid'})[
            1] if bs is not None else np.nan

        gdl_list = game_developers_list.find_all('li',
                                                 {'class': 'c-gameDetails_listItem g-color-gray70 u-inline-block'})

        for i in range(len(gdl_list)):
            gd_treated = gdl_list[i].text.replace("\n", "").strip()
            gdl.append(gd_treated)
    except Exception as e:
        gdl = np.nan
    developers.append(gdl)

    gpbl = []
    try:
        game_publishers_list = bs.find_all('span', {
            'class': 'g-outer-spacing-left-medium-fluid g-color-gray70 u-block'}) if bs is not None else np.nan

        for i in range(len(game_publishers_list)):
            if i != 0:
                gpbl.append(game_publishers_list[i].text)
    except Exception as e:
        gpbl = np.nan
    publishers.append(gpbl)

    ggl = []
    game_genres_list = bs.find('li', {'class': 'c-genreList_item'}) if bs is not None else np.nan
    try:
        ggl_list = game_genres_list.find_all('a')

        for i in range(len(ggl_list)):
            gg_treated = ggl_list[i].text.replace("\n", "").strip()
            ggl.append(gg_treated)
    except Exception as e:
        ggl = np.nan
    genres.append(ggl)

    gs = ""
    game_summary = bs.find('span',
                           {'class': 'c-productionDetailsGame_description g-text-xsmall'}) if bs is not None else np.nan
    try:
        gs = game_summary.text if len(game_summary) > 0 else np.nan
    except Exception as e:
        gs = np.nan
    summaries.append(gs)

    grl = []
    game_rating_list = bs.find(
        class_='c-productionDetailsGame_esrb_title u-inline-block g-outer-spacing-left-medium-fluid')
    try:
        grl_list = game_rating_list.find_all('span') if game_rating_list is not None else np.nan
        for i in range(len(grl_list)):
            grl_treated = grl_list[i].text.replace("\n", "").strip()
            grl.append(grl_treated)
    except Exception as e:
        grl = np.nan
    ratings.append(grl)

    scrape_date.append(datetime.now())

    url.append(all_urls_list[j])

    all_urls_list_aux.remove(all_urls_list[j])

    if (j + 1) % 2400 == 0 and j != 0:
        salva_parte_do_json(names, meta_scores, user_scores, platforms, release_dates, developers, publishers, genres,
                            summaries, ratings, url, scrape_date)

        remove_urls_from_json(all_urls_list_aux)

        file_page_number += 1

    j += 1

# Para o caso da última página não conter 2400 jogos
if len(names) != 0:
    salva_parte_do_json(names, meta_scores, user_scores, platforms, release_dates, developers, publishers, genres,
                        summaries, ratings, url, scrape_date)
    remove_urls_from_json(all_urls_list_aux)
