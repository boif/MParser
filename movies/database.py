import os
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Загрузка переменных окружения из файла .env
load_dotenv()

Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    director = Column(String)
    imdb_rating = Column(Float)
    description = Column(String)

# Получение данных для подключения из переменных окружения
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Настройка базы данных
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()