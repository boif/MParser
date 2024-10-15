from movies.models import Movie
from django.shortcuts import render, redirect
from movies.parser import parse_movie_details
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Настройки для Selenium
options = Options()
options.add_argument("--headless")  # Включаем headless режим
options.add_argument("--disable-gpu")  # Отключаем GPU для стабильности
options.add_argument("--no-sandbox")
service = Service('geckodriver')


def load_movies(request):
    """Загружает фильмы, парсит их и сохраняет в базу данных."""
    if request.method == 'POST':
        # Получаем список всех URL фильмов
        movie_urls = get_all_movie_urls()

        # Парсинг каждой страницы фильма
        movies_data = [parse_movie_details(movie_url) for movie_url in movie_urls]

        # Сортируем фильмы по рейтингу IMDb
        movies_data.sort(key = lambda x: x['rating_imdb'], reverse = True)

        # Очистка старых данных и добавление новых
        Movie.objects.all().delete()  # Удаляем старые данные перед загрузкой новых

        # Сохраняем фильмы в базу данных
        for movie in movies_data:
            Movie.objects.create(
                title = movie['title'],
                year = movie['year'],
                director = movie['director'],
                imdb_rating = movie['rating_imdb'],
                description = movie['description'],
                poster = movie['poster'],
            )

        return redirect('movies_view')


def get_all_movie_urls(max_movies = 100):
    """Получает URL всех фильмов с прокруткой страницы."""
    url = 'https://www.film.ru/online'
    driver = webdriver.Firefox(service = service, options = options)
    driver.get(url)

    movie_urls = []

    def scroll_page(driver):
        """Прокручивает страницу и собирает URL фильмов."""
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(movie_urls) < max_movies:
            # Прокрутка до конца страницы
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(1)

            new_height = driver.execute_script("return document.body.scrollHeight")

            # Парсим HTML после прокрутки
            soup = BeautifulSoup(driver.page_source, 'lxml')
            for movie_block in soup.select('div.redesign_afisha_movie'):
                link_to_movie = movie_block.select_one('a.wrapper_block_stack')['href']
                movie_url = f'https://www.film.ru{link_to_movie.replace("/online", "")}'
                if movie_url not in movie_urls:
                    movie_urls.append(movie_url)

                # Остановка, если собрали достаточное количество фильмов
                if len(movie_urls) >= max_movies:
                    break

            # Если высота страницы не изменилась — выходим из цикла
            if new_height == last_height:
                break
            last_height = new_height

    # Прокручиваем страницу и собираем URL фильмов
    scroll_page(driver)

    driver.quit()
    return movie_urls


def movies_view(request):
    """Отображает страницу с фильмами."""
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})
