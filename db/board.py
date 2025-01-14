import datetime
from db.connection_manager import get_cursor
from loguru import logger


def get_boards():
    query = "SELECT * FROM boards"
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to fetch boards")
        return {"count": 0, "boards": []}
    else:
        return {"count": cursor.rowcount, "boards": rowdicts}


def post_board(new_board_name, new_board_user_id):
    dt_now = datetime.datetime.now()
    query = f"""INSERT INTO boards (board_name, created_at, last_updated_at, status_id, user_id)
                VALUES ('{new_board_name}', '{dt_now}', '{dt_now}', 1, '{new_board_user_id}')
                RETURNING *"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to create a new board")
        return {"count": 0, "boards": []}
    else:
        return {"count of added boards": cursor.rowcount, "boards added": rowdicts}


def del_board(del_board_name):
    query = f"""DELETE FROM boards WHERE board_name = '{del_board_name}' RETURNING *"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            deleted_rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in deleted_rows]
    except Exception:
        logger.exception("Failed to delete the board")
        return {"count": 0, "boards": []}
    else:
        return {"count of deleted boards": cursor.rowcount, "boards": rowdicts}
