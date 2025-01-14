from db.connection_manager import get_cursor
from loguru import logger


def get_users():
    query = "SELECT user_name AS username FROM users"
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to fetch users")
        return {"count": 0, "users": []}
    else:
        return {"count": cursor.rowcount, "users": rowdicts}