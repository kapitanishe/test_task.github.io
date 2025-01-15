import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from config import Config


def get_connection():
    return psycopg2.connect(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        database=Config.DB_NAME
    )


@contextmanager
def get_cursor():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=DictCursor)  # DictCursor возвращает строки в виде словарей
        yield cursor
        connection.commit()  # Фиксируем изменения в случае успешного выполнения
    except Exception as e:
        if connection:
            connection.rollback()  # Откатываем изменения при ошибке
        raise e
    finally:
        if cursor:
            cursor.close()  # Закрываем курсор
        if connection:
            connection.close()  # Закрываем соединение
