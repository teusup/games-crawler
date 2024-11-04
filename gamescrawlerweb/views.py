import numpy as np
import pandas as pd

from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from functools import reduce

from django.views.decorators.csrf import csrf_exempt

from app.games_finder import shift_first_column, pk_meta, pk_ign, pk_gog, df
from gamescrawlerweb.utils import calculate_average_score

df = []
result_list = []


def get_list(request):
    with open("app/dados/result_metacritic.json", "r") as f:
        search_meta = f.read()

    df_meta = pd.read_json(search_meta)

    df_meta = df_meta.drop_duplicates(subset=["URL"], keep="last")

    del df_meta["index"]

    for k, v in df_meta["URL"].items():
        pk_meta.append(v.split("/")[-2])

    df_meta["PK"] = pk_meta
    pk_meta.clear()

    shift_first_column(df_meta)

    with open("app/dados/result_ign.json", "r") as f:
        search_ign = f.read()

    df_ign = pd.read_json(search_ign)

    del df_ign["index"]

    for k, v in df_ign["URL"].items():
        pk_ign.append(v.split("/")[-1])

    df_ign["PK"] = pk_ign

    pk_ign.clear()

    shift_first_column(df_ign)

    with open("app/dados/result_gog.json", "r") as f:
        search_gog = f.read()

    df_gog = pd.read_json(search_gog)

    for k, v in df_gog["URL"].items():
        pk_gog.append(v.split("/")[-1].replace("_", "-"))

    df_gog["PK"] = pk_gog

    pk_gog.clear()

    date_gog = []
    for index, row in df_gog.iterrows():
        ts = int(row["Scrape_date"]) / 1000
        date_gog.append(
            datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        )

    df_gog["Scrape_date"] = date_gog

    date_gog.clear()

    shift_first_column(df_gog)

    df_all = [df_meta, df_ign, df_gog]

    final_df = reduce(
        lambda left, right: pd.merge(left, right, on=["PK"], how="outer"), df_all
    )

    final_df = final_df.fillna(np.nan)

    global df

    df = final_df.drop_duplicates(subset=["PK"], keep="first")

    return render(request, "index.html", get_context(request, df))


@csrf_exempt
def search(request):
    regex = request.POST.get("search").lower()
    regex_type = request.POST.get("search-type")

    dataframe = pd.DataFrame()

    match regex_type:
        case "s-all-columns":
            textlikes = df.select_dtypes(include=[object, "string"])
            dataframe = df[
                textlikes.apply(
                    lambda column: column.str.contains(
                        regex, regex=True, case=False, na=False
                    )
                ).any(axis=1)
            ]
        case "s-game-name":
            dataframe = df[
                (df["Game_name_x"].str.lower().str.contains(regex))
                | (df["Game_name_y"].str.lower().str.contains(regex))
                | (df["Game_name"].str.lower().str.contains(regex))
            ]
        case "s-genre":

            def combine_genres(row):
                genres = [row["Genres_x"], row["Genres_y"], row["Genre"]]
                combined_genres = "; ".join(
                    [str(genre) for genre in genres if genre is not None]
                )  # Combine non-missing genres
                return combined_genres

            df["Combined_Genres"] = df.apply(combine_genres, axis=1)
            dataframe = df[(df["Combined_Genres"].str.lower().str.contains(regex))]
        case "s-developer-publisher":

            def combine_dev_pub(row):
                union_dev_pub = [
                    row["Publisher_x"],
                    row["Publisher_y"],
                    row["Developer_x"],
                    row["Developer_y"],
                    row["Company"],
                    row["Release_date_x"],
                ]
                combined_dev_pub = "; ".join(
                    [
                        str(dev_pub_com)
                        for dev_pub_com in union_dev_pub
                        if dev_pub_com is not None
                    ]
                )
                return combined_dev_pub

            df["Combined_Developers_Publishers"] = df.apply(combine_dev_pub, axis=1)
            dataframe = df[
                (df["Combined_Developers_Publishers"].str.lower().str.contains(regex))
            ]
        case "s-release-year":
            if regex.isdigit():
                dataframe = df[
                    df["Release_date_x"].notna()
                    & df["Release_date_x"].str.contains(regex)
                    | df["Release_date_y"].notna()
                    & df["Release_date_y"].str.contains(regex)
                ]

    global result_list
    result_list = dataframe.to_dict(orient="records")

    return redirect("result")


def result(request):

    results_list = result_list
    if results_list is None:
        return redirect("search")

    paginator = Paginator(results_list, 10)  # Mostra 10 resultados por página

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    dtframe_lines = len(results_list)

    context = {"dtframe_lines": dtframe_lines, "page_obj": page_obj}
    return render(request, "result.html", context)


def get_context(request, dtframe):
    # Pagination settings
    page_number = request.GET.get("page", 1)
    paginator = Paginator(
        dtframe.to_dict(orient="records"), 10
    )  # Assuming 10 items per page

    page_obj = paginator.get_page(page_number)

    dtframe_lines = len(dtframe)

    context = {
        "dtframe_lines": dtframe_lines,
        "page_obj": page_obj,
        "columns": dtframe.columns,
    }

    return context


def game_details(request, primary_key):
    try:
        gd = df[df["PK"] == primary_key]
        average_score = calculate_average_score(gd.iloc[0])
    except IndexError:
        gd = None
        average_score = None

    return render(
        request,
        "game_details.html",
        {"game_details": gd.iloc[0], "average_score": average_score},
    )
