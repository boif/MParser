import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

BASE_URL = 'https://www.film.ru/online'


def parse_movie_details(movie_url):
    # Запрос на получение страницы фильма
    response = requests.get(movie_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    # Извлечение названия и года
    title_with_year = soup.select_one('h1').get_text(strip=True)
    title = re.sub(r'\s*\(.*?\)\s*', '', title_with_year)  # Удаление года из названия
    year = soup.select_one('h1 span').get_text(strip=True)

    # Извлечение рейтинга IMDb
    rating_elements = soup.select('.wrapper_movies_scores_score')
    if len(rating_elements) > 1:
        rating_text = rating_elements[1].get_text(strip=True)
        rating_imdb_match = re.search(r'\d+\.\d+', rating_text)
        rating_imdb = float(rating_imdb_match.group(0)) if rating_imdb_match else 0.0
    else:
        rating_imdb = 0.0  # Значение по умолчанию, если рейтинг отсутствует

    # Извлечение режиссера
    director_element = soup.select_one('.block_table:-soup-contains("режиссер") + div a')
    director = director_element.get_text(strip=True) if director_element else None

    # Описание фильма
    description = soup.select_one('.wrapper_movies_text').get_text(strip=True)

    # Извлечение ссылки на постер
    poster_tag = soup.select_one('.wrapper_block_stack.wrapper_movies_poster')
    poster_url = urljoin(movie_url, poster_tag['data-src']) if poster_tag and 'data-src' in poster_tag.attrs else None

    poster_path = None
    if poster_url:
        # Скачивание постера
        poster_response = requests.get(poster_url)
        poster_response.raise_for_status()

        # Создание директории для хранения постеров
        os.makedirs('media/movies/posters', exist_ok=True)

        # Форматирование имени файла постера
        poster_name = f"{title.replace(' ', '_').replace('/', '-')}.jpg"
        poster_path = os.path.join('media/movies/posters', poster_name)

        # Сохранение постера на диск
        with open(poster_path, 'wb') as poster_file:
            poster_file.write(poster_response.content)

    return {
        'title': title,
        'year': year,
        'rating_imdb': rating_imdb,
        'director': director,
        'description': description,
        'poster': poster_path,
    }


def parse_movies_list():
    # Запрос на главную страницу с фильмами
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    # Поиск всех блоков с фильмами
    movies = []
    for movie_block in soup.select('div.redesign_afisha_movie'):
        link_to_movie = movie_block.select_one('a.wrapper_block_stack')['href']
        movie_url = urljoin('https://www.film.ru', link_to_movie.replace('/online', ''))

        # Парсинг деталей каждого фильма
        movie_details = parse_movie_details(movie_url)
        movies.append(movie_details)

    return movies


if __name__ == "__main__":
    movies = parse_movies_list()
    # Здесь можно добавить код для дальнейшей обработки фильмов (например, сохранение в базу данных)
