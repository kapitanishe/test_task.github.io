from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()  #TODO: убрать при deploy


class Config:
    # Настройки базы данных
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
