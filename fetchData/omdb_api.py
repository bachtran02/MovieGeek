import json
import requests
import os


# get ratings & actors & directors # release date # domestic box office
def omdb_search(name='Avengers Endgame', year=2019):
    api_key = os.environ.get('OMDb_API_KEY')
    url = 'https://www.omdbapi.com'
    params = (
        ('t', name),
        ('y', year),
        ('apikey', api_key)
    )

    response = requests.get(url, params=params)
    json_data = json.loads(response.text)

    if json_data['Response'] == 'False':
        return False

    imdb_r = json_data['imdbRating']
    rt_r, mc_r = config_rating(json_data)
    ratings = f"IMDB: {imdb_r}\nRotten Tomatoes: {rt_r}\nMetaCritic: {mc_r}"

    awards = json_data['Awards']
    rated = json_data['Rated']

    director_str = config_str(json_data['Director'])
    actor_str = config_str(json_data['Actors'])

    d_bo = config_revenue(json_data['BoxOffice'])
    release = json_data['Released']

    return release, rated, director_str, actor_str, d_bo, awards, ratings


def config_rating(json_data):
    rotten_tomatoes = "N/A"
    metacritic = "N/A"

    rating_list = json_data['Ratings']

    len_rl = len(rating_list)

    if len_rl >= 3:
        rotten_tomatoes = json_data['Ratings'][1]['Value']
        metacritic = json_data['Ratings'][2]['Value']
    elif len_rl == 2:
        rotten_tomatoes = json_data['Ratings'][1]['Value']
        metacritic = "Unknown"

    return rotten_tomatoes, metacritic


def config_str(instr):
    if ',' not in instr:
        return instr

    li = [x.strip() for x in instr.split(',')]

    if len(li) == 2:
        string = f"{li[0]},\n{li[1]}"
    else:
        string = f"{li[0]},\n{li[1]},\n{li[2]}"
        if len(li) > 3:
            string = string + ", et al"

    return string


def config_revenue(revenue):
    revenue = str(revenue)
    if len(revenue) < 9:
        return ""

    return f'(US: {revenue[:revenue.find(",")]}M)'

