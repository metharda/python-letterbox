import subprocess
import veritabani as vt

## Geçiş fonksiyonları:
def anaSayfa():
        subprocess.run(["python", "anaSayfa.py"], check=True)
def filmEkleSayfasi():
        subprocess.run(["python", "filmEkle.py"], check=True)
def filmListeSayfasi():
        subprocess.run(["python", "filmListe.py"], check=True)
def incelemeEklemeSayfasi():
        subprocess.run(["python", "incelemeEkle.py"], check=True)
def incelemeListelemeSayfasi():
        subprocess.run(["python", "incelemeListe.py"], check=True)

## Veritabanı işlemleri:
def filmEkle(medya, ad, izlenme):
        film = {}
        ad = ' '.join(word.capitalize() for word in ad.split())
        if medya == "Film":
                film[ad] = {
                        "Medya Tipi": medya,
                        f"{medya} Türü": filmBul(ad)["genre"],
                        "Banner": filmBul(ad)["banner"],
                        "Özet": filmBul(ad)["summary"],
                        "İzlenme Durumu": izlenme
                }
        else:
                film[ad] = {
                        "Medya Tipi": medya,
                        f"{medya} Türü": diziBul(ad)["genre"],
                        "Banner": diziBul(ad)["banner"],
                        "Özet": diziBul(ad)["summary"],
                        "İzlenme Durumu": izlenme
                }
        vt.filmEkle(film)


def incelemeEkle(film,puan,yorum):
    inceleme={}
    inceleme[film]={
        "Puan": puan,
        "Yorum": yorum
    }
    vt.incelemeEkle(film,inceleme)


def filmSil(film):
    vt.filmSil(film)

        
def incelemeSil(film):
    vt.incelemeSil(film)

def filmBul(film):
    film_bilgileri = vt.get_movie_details(film)
    if film_bilgileri:
        banner_url = f"https://image.tmdb.org/t/p/w500{film_bilgileri['poster_path']}" if film_bilgileri.get('poster_path') else ""
        genre_ids = film_bilgileri['genre_ids']
        genre_names = vt.get_genre_names()
        genres = [genre_names.get(genre_id, "Unknown") for genre_id in genre_ids]
        return {
        'title': film_bilgileri['original_title'],
        'genre': ', '.join(genres),
        'summary': film_bilgileri['overview'],
        'banner': banner_url
        }
    else:
        return None
    
def diziBul(dizi):
    dizi_bilgileri = vt.get_series_details(dizi)
    if dizi_bilgileri:
        banner_url = f"https://image.tmdb.org/t/p/w500{dizi_bilgileri['poster_path']}" if dizi_bilgileri.get('poster_path') else ""
        genre_ids = dizi_bilgileri['genre_ids']
        genre_names = vt.get_series_genre_names()
        genres = [genre_names.get(genre_id, "Unknown") for genre_id in genre_ids]
        return {
        'title': dizi_bilgileri['original_name'],
        'genre': ', '.join(genres),
        'summary': dizi_bilgileri['overview'],
        'banner': banner_url
        }
    else:
        return None
    

if __name__ == "__main__":
    anaSayfa()