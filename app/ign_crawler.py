import json
import numpy as np
import pandas as pd
import tqdm

from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from requests import get

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

names = []
ign_scores = []
user_scores = []
summary = []
age_ratings = []
content_ratings_info = []
developers = []
publishers = []
franchises = []
features = []
initial_releases = []
platforms = []
genres = []
main_story_hours = []
story_sides_hours = []
everything_hours = []
all_styles_hours = []
urls = []
scrape_date = []

urls_not_in_ign = []

count_urls_in_ign = 1

file_page_number = 1

url_default = 'https://www.ign.com/games/'


def salva_parte_do_json(names_aux, ign_scores_aux, user_scores_aux, summary_aux, age_ratings_aux,
                        content_ratings_info_aux, developers_aux, publishers_aux, franchises_aux, features_aux,
                        initial_releases_aux, platforms_aux, genres_aux, main_story_hours_aux, story_sides_hours_aux,
                        everything_hours_aux, all_styles_hours_aux, urls_aux, scrape_date_aux):
    game_df = pd.DataFrame({'Game_name': names,
                            'Ign_score': ign_scores,
                            'User_score': user_scores,
                            'Summary': summary,
                            'Age_rating': age_ratings,
                            'Content_ratings_info': content_ratings_info,
                            'Developer': developers,
                            'Publisher': publishers,
                            'Franchise': franchises,
                            'Features': features,
                            'Initial_release': initial_releases,
                            'Platforms': platforms,
                            'Genres': genres,
                            'Main_story_hours': main_story_hours,
                            'Story_sides_hours': story_sides_hours,
                            'Everything_hours': everything_hours,
                            'All_styles_hours': all_styles_hours,
                            'URL': urls,
                            'Scrape_date': scrape_date})

    # Opção para preencher os valores NaN
    game_df = game_df.fillna(value=np.nan)

    now = date.today()

    dt_string = now.strftime("%Y_%m_%d")

    file_page_number_format = "{:04d}".format(file_page_number)

    result_ign_file_name = ("dados/result_ign/result_ign_" + dt_string + "_" + file_page_number_format +
                            ".json")

    # Transformando a tabela em um json e importando para um arquivo
    with open(result_ign_file_name, 'w') as f:
        f.write(game_df.to_json(orient='records', date_format='iso'))

    clean_lists()


def clean_lists():
    names.clear()
    ign_scores.clear()
    user_scores.clear()
    summary.clear()
    age_ratings.clear()
    content_ratings_info.clear()
    developers.clear()
    publishers.clear()
    franchises.clear()
    features.clear()
    initial_releases.clear()
    platforms.clear()
    genres.clear()
    main_story_hours.clear()
    story_sides_hours.clear()
    everything_hours.clear()
    all_styles_hours.clear()
    urls.clear()
    scrape_date.clear()


def clean_urls_not_in_ign():
    urls_not_in_ign.clear()


def remove_urls_from_json(all_urls_list_aux_b):
    urls_dataframe = pd.DataFrame({'url': all_urls_list_aux_b})
    with open('dados/result_all_urls_ign.json', 'w') as f:
        f.write(urls_dataframe.to_json())


def salva_parte_do_json_not_in_ign(urls_aux):
    urls_dataframe = pd.DataFrame({'url': urls_aux})

    now = date.today()

    dt_string = now.strftime("%Y_%m_%d")

    file_page_number_format = "{:04d}".format(file_page_number)

    result_urls_not_in_ign_file_name = ("dados/result_ign/urls_not_in_ign/urls_not_in_ign_" + dt_string + "_" +
                                        file_page_number_format + ".json")

    # Transformando a tabela em um json e importando para um arquivo
    with open(result_urls_not_in_ign_file_name, 'w') as f:
        f.write(urls_dataframe.to_json(date_format='iso'))

    clean_urls_not_in_ign()


def remove_text(text):
    num = ""
    for c in text:
        if c.isdigit():
            num = num + c
    return num

# Realiza a leitura do arquivo auxiliador
with open('dados/result_all_urls_ign.json', 'r') as f:
    search = f.read()

# Normaliza o dado para um json
search = json.loads(search)

all_urls_list = []

for k, v in search['url'].items():
    all_urls_list.append(v)

all_urls_list_aux = all_urls_list[:]

# Iniciando o loop de raspagem de dados do IGN
for j in tqdm.tqdm(range(len(all_urls_list)), ncols=100, colour='green', desc="Coleta de dados IGN"):

    url = url_default + all_urls_list[j]

    # Make a get request
    games = get(url, headers=headers)

    while games.status_code != 200 and games.status_code != 404:
        games = get(url, headers=headers)

    try:
        if games.status_code != 404:
            # Parse the game response content into the beautiful soup object
            game_soup = BeautifulSoup(games.text, 'html.parser')

            # Find the major tag peculiar to each game

            # scrape name
            try:
                name = game_soup.find('h1', class_='display-title jsx-1812565333 balanced')
                name = name.text
            except Exception as e:
                name = np.nan

            names.append(name)

            # scrap scores
            try:
                ign_score = game_soup.find('span', class_='hexagon-content-wrapper')
                # print(score.text)
                ign_score = ign_score.text
                ign_score = ign_score if remove_text(ign_score) != '' else np.nan
            except Exception as e:
                ign_score = np.nan

            ign_scores.append(ign_score)

            # scrap scores
            try:
                user_score = game_soup.find_all('h3', class_='title5 jsx-1096646909')
                user_score = user_score[3].text
                user_score = user_score if remove_text(user_score) != '' else np.nan
            except Exception as e:
                user_score = np.nan

            user_scores.append(user_score)

            # scrape summary
            try:
                smry = game_soup.find('div', class_='object-summary-text summary-info')
                smry = smry.text
            except Exception as e:
                smry = np.nan

            summary.append(smry)

            # scrape age rating
            try:
                age_rating = game_soup.find('div', attrs={'class': 'stack jsx-2503409011'})
                age_rating = age_rating.find('svg').text
                age_rating = age_rating.replace('ESRB: ', '')
            except Exception as e:
                age_rating = np.nan

            age_ratings.append(age_rating)

            # scrape content rating info
            try:
                content_rating_info = game_soup.find('div', class_='object-summary-text content-rating-info')
                content_rating_info = content_rating_info.find('div', attrs={'class': 'object-summary-text '
                                                                                      'content-rating-info'})
                content_rating_info = content_rating_info.text
                content_rating_info = content_rating_info.split(", ")
            except Exception as e:
                content_rating_info = np.nan

            content_ratings_info.append(content_rating_info)

            # scrape developer
            gdl = []
            try:
                for a in game_soup.find_all('div', attrs={'class': 'object-summary-text developers-info'}):
                    developer = a.find_all('a', attrs={'class': 'jsx-2126220331 underlined'})
                for i in range(len(developer)):
                    gdl.append(developer[i].text)

            except Exception as e:
                gdl.append(np.nan)

            developers.append(gdl)

            # scrape publisher
            gpl = []
            try:
                for a in game_soup.find_all('div', attrs={'class': 'object-summary-text publishers-info'}):
                    publisher = a.find_all('a', attrs={'class': 'jsx-2126220331 underlined'})
                for i in range(len(publisher)):
                    gpl.append(publisher[i].text)
            except Exception as e:
                gpl.append(np.nan)

            publishers.append(gpl)

            # scrape franchises
            gfl = []
            try:
                for a in game_soup.find_all('div', attrs={'class': 'object-summary-text franchises-info'}):
                    franchise = a.find_all('a', attrs={'class': 'jsx-2126220331 underlined'})
                for i in range(len(franchise)):
                    gfl.append(franchise[i].text)
            except Exception as e:
                gfl.append(np.nan)

            franchises.append(gfl)

            # scrape features
            game_features_list = []
            try:
                for a in game_soup.find_all('div', attrs={'class': 'object-summary-text features-info'}):
                    feature = a.find_all('a', attrs={'class': 'jsx-2126220331 underlined'})
                for i in range(len(feature)):
                    game_features_list.append(feature[i].text)
            except Exception as e:
                game_features_list.append(np.nan)

            features.append(game_features_list)

            # scrape release date
            try:
                initial_release = game_soup.find('div', attrs={'class': 'object-summary-text initial-release-info'})
                initial_release = initial_release.find('div', attrs={'class': 'interface jsx-901232385 small'})
                initial_release = initial_release.text
            except Exception as e:
                initial_release = np.nan

            initial_releases.append(initial_release)

            # scrape platforms
            games_platforms_list = []
            try:
                for a in game_soup.find_all('div', attrs={'class': 'object-summary-text platforms-info'}):
                    platform = a.find_all('a', attrs={'class': 'platform-icon'})
                for i in range(len(platform)):
                    games_platforms_list.append(platform[i].text)
            except Exception as e:
                games_platforms_list.append(np.nan)

            platforms.append(games_platforms_list)

            # scrape genres
            ggl = []
            try:
                for a in game_soup.find_all('div', attrs={'class': 'object-summary-text genres-info'}):
                    genre = a.find_all('a', attrs={'class': 'jsx-2126220331 underlined'})
                for i in range(len(genre)):
                    ggl.append(genre[i].text)
            except Exception as e:
                ggl.append(np.nan)

            genres.append(ggl)

            # scrape main story hour
            try:
                main_story_hour = game_soup.find_all('h4', attrs={'class': 'title4 jsx-1519668320'})
                main_story_hour = main_story_hour[0].text
                main_story_hour = remove_text(main_story_hour)
                main_story_hour = main_story_hour if main_story_hour != '' else np.nan
            except Exception as e:
                main_story_hour = np.nan

            main_story_hours.append(main_story_hour)

            # scrape story side hour
            try:
                story_sides_hour = game_soup.find_all('h4', attrs={'class': 'title4 jsx-1519668320'})
                story_sides_hour = story_sides_hour[1].text
                story_sides_hour = remove_text(story_sides_hour)
                story_sides_hour = story_sides_hour if story_sides_hour != '' else np.nan
            except Exception as e:
                story_sides_hour = np.nan

            story_sides_hours.append(story_sides_hour)

            # scrape everything hour
            try:
                everything_hour = game_soup.find_all('h4', attrs={'class': 'title4 jsx-1519668320'})
                everything_hour = everything_hour[2].text
                everything_hour = remove_text(everything_hour)
                everything_hour = everything_hour if everything_hour != '' else np.nan
            except Exception as e:
                everything_hour = np.nan

            everything_hours.append(everything_hour)

            # scrape all styles hour
            try:
                all_styles_hour = game_soup.find_all('h4', attrs={'class': 'title4 jsx-1519668320'})
                all_styles_hour = all_styles_hour[3].text
                all_styles_hour = remove_text(all_styles_hour)
                all_styles_hour = all_styles_hour if all_styles_hour != '' else np.nan
            except Exception as e:
                all_styles_hour = np.nan
            all_styles_hours.append(all_styles_hour)

            try:
                urls.append(url)
            except Exception as e:
                urls.append(np.nan)

            scrape_date.append(datetime.now())

            all_urls_list_aux.remove(all_urls_list[j])

            if count_urls_in_ign % 2400 == 0:
                salva_parte_do_json_not_in_ign(urls_not_in_ign)
                salva_parte_do_json(names, ign_scores, user_scores, summary, age_ratings, content_ratings_info,
                                    developers,
                                    publishers, franchises, features, initial_releases, platforms, genres,
                                    main_story_hours,
                                    story_sides_hours, everything_hours, all_styles_hours, urls, scrape_date)
                remove_urls_from_json(all_urls_list_aux)

                file_page_number += 1

            count_urls_in_ign += 1

        else:
            urls_not_in_ign.append(url)

            all_urls_list_aux.remove(all_urls_list[j])

        j += 1

    except Exception as e:
        print(url)
        print(e)

# Para o caso da última página não conter 2400 jogos
if len(names) != 0:
    salva_parte_do_json_not_in_ign(urls_not_in_ign)
    salva_parte_do_json(names, ign_scores, user_scores, summary, age_ratings, content_ratings_info, developers,
                        publishers, franchises, features, initial_releases, platforms, genres, main_story_hours,
                        story_sides_hours, everything_hours, all_styles_hours, urls, scrape_date)
    remove_urls_from_json(all_urls_list_aux)
