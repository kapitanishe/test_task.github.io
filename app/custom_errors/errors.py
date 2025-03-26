class DataValidationError(Exception):
    """Ошибка валидации"""


class UnauthorizedError(Exception):
    """Ошибка авторизации"""


class RoleError(UnauthorizedError):
    """Ошибка прав пользователя"""


class DBError(Exception):
    pass


class UniqueError(DBError):
    """Введено неуникальное название"""


class DataGetError(DBError):
    """Ошибка get запроса"""


class DeletionError(DBError):
    """Ошибка при удалении доски из БД"""


class UpdateError(DBError):
    """Ошибка при обновлении объекта"""


class StatusError(DBError):
    """Ошибка статуса карточки"""


class StatusNotFoundError(DBError):
    """Нет такого статуса карточки"""


class RecordNotFoundError(DBError):
    """Запись отсутсвует в БД"""


class BoardNotFoundError(DBError):
    """Доска отсутствует в БД"""


class CardNotFoundError(DBError):
    """Карточка отсутствует в БД"""


class CardUpdateNotFoundError(DBError):
    """Обновленная карточка отсутствует в БД"""


class MatchNotFoundError(DBError):
    """Запись отсутсвует в БД"""


class EstimationCounterError(Exception):
    """Ошибка вычисления суммы длительности выполнения карточек"""
