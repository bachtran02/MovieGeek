import json
import requests
import os
from io import BytesIO
from PIL import Image


def tmdb_search(name='Avengers Endgame', index=0):
    api_key = os.environ.get('TMDB_API_KEY')
    url = 'https://api.themoviedb.org/3/search/movie'
    image_base_url = 'https://image.tmdb.org/t/p/w500'
    params = (
        ('api_key', api_key),
        ('language', 'en-US'),
        ('include_adult', 'false'),
        ('query', name),
    )

    response = requests.get(url, params=params)
    json_data = json.loads(response.text)

    if len(json_data['results']) == 0:
        return False

    movie_id = json_data['results'][index]['id']

    id_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    dif_params = (
        ('api_key', api_key),
        ('append_to_response', 'videos')
    )

    res = requests.get(id_url, params=dif_params)
    data = json.loads(res.text)

    released = True if data['status'] == 'Released' else False
    title = data['title']
    year = data['release_date'][:4]
    runtime = str(data['runtime']) + ' min'
    genres = get_genres(data)
    t_bo = '$' + str("{:,}".format(int(data['revenue'])))
    overview = data['overview']

    poster_url = image_base_url + data['poster_path'] \
        if data['poster_path'] is not None else os.environ.get('GIF_address_1')
    comp_url = data['production_companies'][0]['logo_path']
    comp_url = image_base_url + comp_url if comp_url is not None else os.environ.get('GIF_address_2')
    trailer_url = get_trailer_url(data) if get_trailer_url(data) is not False else "N/A"
    color_tuple = config_img(poster_url)

    return released, title, runtime, genres, t_bo, overview, poster_url, comp_url, trailer_url, color_tuple, year


def get_genres(data):

    l = data['genres']
    n = len(l) if len(l) <= 3 else 3
    string = ""

    for i in range(n):
        if i == n - 1:
            string += l[i]['name']
        else:
            string += l[i]['name'] + '\n'

    return string


def get_trailer_url(data):
    found = False
    key = ""
    for i in reversed(data['videos']['results']):
        if i['type'] == 'Trailer' and i['site'] == 'YouTube':
            key = i['key']
            found = True
            break

    if found is True:
        return 'https://www.youtube.com/watch?v=' + key

    return False


def config_img(image_url):
    if image_url.endswith('.gif'):
        return [255, 255, 255]

    resp = requests.get(image_url)
    # assert resp.ok
    img = Image.open(BytesIO(resp.content))
    img2 = img.resize((1, 1))

    color = img2.getpixel((0, 0))

    return color


