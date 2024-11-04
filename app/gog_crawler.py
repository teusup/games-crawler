import json
import numpy as np
import pandas as pd
import re
import tqdm

from bs4 import BeautifulSoup
from datetime import datetime
from requests import get

name_list = []
score_list = []
price_list = []
description_list = []
genre_list = []
tags_list = []
works_on_list = []
release_date_list = []
company_list = []
size_list = []
links_list = []
rating_list = []
game_features_list = []
audio_languages_list = []
text_languages_list = []
requirements_list = []
opencritic_average_list = []
opencritic_recommended_list = []
scrape_date_list = []
url_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.127 Safari/537.36'}

# Realiza a leitura do arquivo auxiliador
with open('dados/result_all_urls_gog.json', 'r') as f:
    search = f.read()

# Normaliza o dado para um json
search = json.loads(search)

all_urls_list = []

for k, v in search['url'].items():
    all_urls_list.append(v)

for j in tqdm.tqdm(range(len(all_urls_list)), ncols=100, colour="green", desc="Coleta de dados individuais"):

    webpage = get(all_urls_list[j], headers=headers)

    # Fazendo requisição até retornar o html
    while len(webpage.text) == 0:
        webpage = get(all_urls_list[j], headers=headers)

    bs = BeautifulSoup(webpage.text, 'html.parser')

    gn = ""
    try:
        gn = bs.find('h1').text.replace("\n", "").strip()
    except Exception as e:
        gn = np.nan
    name_list.append(gn)

    gs = ""
    try:
        gs = bs.find('div', class_='rating productcard-rating__score').text.split('/')[0]
    except Exception as e:
        gs = np.nan
    score_list.append(gs)

    gp = ""
    try:
        gp = bs.find('span', class_='product-actions-price__final-amount').text
    except Exception as e:
        gp = np.nan
    price_list.append(gp)

    gd = ""
    try:
        gd = bs.find('div', class_='description').text.replace("\n", "").strip()
        gd = re.sub(' +', ' ', gd)
        gd = gd.replace("This game is part of your Welcome Offer! Get this game for a special price just for you!Find "
                        "more excellent games at great discounts : : ", "")
    except Exception as e:
        gd = np.nan
    description_list.append(gd)

    gg = []
    try:
        game_genre = bs.find(string='Genre:').findNext("div").find_all('a')

        for i in range(len(game_genre)):
            gg.append(game_genre[i].text)
    except Exception as e:
        gg = np.nan
    genre_list.append(gg)

    gt = []
    try:
        game_tag = bs.find(string='Tags:').findNext("div").find_all('a')

        for i in range(len(game_tag)):
            gt.append(game_tag[i].text)
    except Exception as e:
        gt = np.nan
    tags_list.append(gt)

    gwo = []
    try:
        gwo = bs.find(string='\n                            Works on:\n                    ').findNext("div").text
        gwo = gwo.replace("\n", "").strip()
    except Exception as e:
        gwo = np.nan
    works_on_list.append(gwo)

    grd = []
    try:
        grd = bs.find(string='\n                            Release date:\n                    ').findNext("div").text
    except Exception as e:
        grd = np.nan
    release_date_list.append(grd)

    gc = []
    try:
        game_company = (bs.find(string='\n                        Company:\n                ').findNext("div")
                        .find_all('a'))

        for i in range(len(game_company)):
            gc.append(game_company[i].text)
    except Exception as e:
        gc = np.nan
    company_list.append(gc)

    gsz = ""
    try:
        gsz = bs.find(string='\n                            Size:\n                    ').findNext("div").text
        gsz = gsz.replace("\n", "").strip()
    except Exception as e:
        gsz = np.nan
    size_list.append(gsz)

    gl = []
    try:
        game_links = (bs.find(string='\n                            Links:\n                    ').findNext("div")
                      .find_all('a'))

        for i in range(len(game_links)):
            gl.append(game_links[i].get('href'))
    except Exception as e:
        gl = np.nan
    links_list.append(gl)

    gr = ""
    try:
        gr = bs.find('div', class_='age-restrictions').text
        gr = gr.replace("\n", "").strip()
        gr = gr.replace("\r", "").strip()
    except Exception as e:
        gr = np.nan
    rating_list.append(gr)

    gf = []
    try:
        gf.append(bs.find(string='\n                                    Game features\n                          '
                                 '  ').findNext("div").text.replace("\n", "").strip())
        game_features = bs.find_all('div', class_='table__row details__rating details__row details__row--without-label')

        for i in range(len(game_features)):
            gf.append(game_features[i].text.replace("\n", "").strip())
    except Exception as e:
        gf = np.nan
    game_features_list.append(gf)

    gal = []
    try:
        game_audio_languages = bs.find_all('div', class_='details__languages-row--cell '
                                                         'details__languages-row--language-name')

        for i in range(len(game_audio_languages)):
            if bs.find(string=game_audio_languages[i].text).findNext("div")['class'] == ['details__languages-row--cell',
                                                                                         'details__languages-row'
                                                                                         '--audio-support']:
                gal.append(game_audio_languages[i].text.replace("\n", "").strip())
    except Exception as e:
        gal = np.nan
    audio_languages_list.append(gal)

    gtl = []
    try:
        game_text_languages = bs.find_all('div', class_='details__languages-row--cell '
                                                        'details__languages-row--language-name')

        for i in range(len(game_text_languages)):
            if (bs.find(string=game_text_languages[i].text).findNext("div").findNext("div")['class'] ==
                    ['details__languages-row--cell', 'details__languages-row--text-support']):
                gtl.append(game_text_languages[i].text.replace("\n", "").strip())
    except Exception as e:
        gtl = np.nan
    text_languages_list.append(gtl)

    grq = []
    try:
        game_req = bs.find_all('script')
        for i in range(len(game_req)):
            if game_req[i].get(
                    'src') == "https://menu-static.gog-statics.com/assets/js/v2/gog-module-topic-parsers_min.js":
                grq = \
                game_req[i + 1].text.split("window.productcardData.cardProductSystemRequirements = ")[1].split(";")[0]
                break
    except Exception as e:
        grq = np.nan
    requirements_list.append(grq)

    goa = ""
    try:
        goa = bs.find('div', class_='critics-ratings')
        goa = goa.find('span', class_='circle-score__text').text.replace("\n", "").strip()
    except Exception as e:
        goa = np.nan
    opencritic_average_list.append(goa)

    gor = ""
    try:
        gor = bs.find_all('div', class_='critics-rating-wrapper')[1]
        gor = gor.find('span', class_='circle-score__text').text.replace("\n", "").replace("%", "").strip()
    except Exception as e:
        gor = np.nan
    opencritic_recommended_list.append(gor)

    scrape_date_list.append(datetime.now())

    url_list.append(all_urls_list[j])

game_df = pd.DataFrame({'Game_name': name_list,
                        'Score': score_list,
                        'Price': price_list,
                        'Description': description_list,
                        'Genre': genre_list,
                        'Tag': tags_list,
                        'Works_on': works_on_list,
                        'Release_date': release_date_list,
                        'Company': company_list,
                        'Size': size_list,
                        'Link': links_list,
                        'Rating': rating_list,
                        'Game_features': game_features_list,
                        'Audio_languages': audio_languages_list,
                        'Text_languages': text_languages_list,
                        'Requirements': requirements_list,
                        'OpenCritic_average': opencritic_average_list,
                        'OpenCritic_recommended': opencritic_recommended_list,
                        'URL': url_list,
                        'Scrape_date': scrape_date_list})

# Opção para preencher os valores NaN
game_df = game_df.fillna(value=np.nan)

with open('dados/result_gog.json', 'w') as f:
    f.write(game_df.to_json(orient='records'))
