import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

database = {}
def veritabani_kaydet():
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=4)

def veritabani_yukle():
    global database
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
    except FileNotFoundError:
        print("Veritabanı bulunamadı")
        database = {}


def filmEkle(film):
    global database
    veritabani_yukle()
    database.update(film)
    veritabani_kaydet()


def incelemeEkle(film_adi, inceleme):
    global database
    veritabani_yukle()
    if film_adi in database:
        if 'incelemeler' not in database[film_adi]:
            database[film_adi]['incelemeler'] = []
        database[film_adi]['incelemeler'].append(inceleme)
    else:
        print(f"{film_adi} isimli film bulunamadı.")
    veritabani_kaydet()


def filmSil(film_adi):
    global database
    veritabani_yukle()
    if film_adi in database:
        del database[film_adi]
    else:
        print(f"{film_adi} isimli film bulunamadı.")
    veritabani_kaydet()

    
def incelemeSil(film):
    global database
    veritabani_yukle()
    for film in database:
        if 'incelemeler' in database[film]:
            del database[film]['incelemeler']
    veritabani_kaydet()

## tmdb API
api_key = os.getenv("TMDB_API_KEY")
def get_movie_details(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}&language=tr"
    response = requests.get(url)
    
    if response.status_code == 200:
        search_results = response.json()
        if search_results['results']:
            movie_data = search_results['results'][0]
            return movie_data
        else:
            print("Film bulunamadı.")
            return None
    else:
        print("API hatası oluştu.")
        return None

def get_series_details(series_name):
    url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={series_name}&language=tr"
    response = requests.get(url)
    
    if response.status_code == 200:
        search_results = response.json()
        if search_results['results']:
            series_data = search_results['results'][0]
            return series_data
        else:
            print("Dizi bulunamadı.")
            return None
    else:
        print("API hatası oluştu.")
        return None
    
def get_genre_names():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=tr"
    try:
        response = requests.get(url)
        response.raise_for_status()
        genre_data = response.json()
        genre_names = {genre['id']: genre['name'] for genre in genre_data['genres']}
        return genre_names
    except requests.exceptions.HTTPError as err:
        print(f"HTTP hata oluştu: {err}")
        return {}
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")
        return {}

def get_series_genre_names():
    url = f"https://api.themoviedb.org/3/genre/tv/list?api_key={api_key}&language=tr"
    try:
        response = requests.get(url)
        response.raise_for_status()
        genre_data = response.json()
        genre_names = {genre['id']: genre['name'] for genre in genre_data['genres']}
        return genre_names
    except requests.exceptions.HTTPError as err:
        print(f"HTTP hata oluştu: {err}")
        return {}
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")
        return {}