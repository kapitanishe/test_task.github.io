import datetime

from loguru import logger

from db.connection_manager import get_cursor
from time_counter import TimeCounter


def get_cards():
    query = "SELECT * FROM cards"
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row, strict=False)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to fetch cards")
        return {"count": 0, "cards": []}
    else:
        return {"count": cursor.rowcount, "cards": rowdicts}


def post_card(new_card, new_card_board, card_description, card_estimation):
    dt_now = datetime.datetime.now()
    query_board_id = "SELECT board_id FROM boards WHERE board_name = %s"
    params_board_id = (new_card_board,)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_board_id, params_board_id)
            board_id = cursor.fetchone()[0]
    except Exception:
        logger.exception("Failed to get board_id by board_name")
        return "Unknown error", 500
    query_post_card = """
        INSERT INTO cards (assignee, board, created_at, description, estimation, status, title)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;"""
    params_post_card = (1, board_id, dt_now, card_description, card_estimation, 1, new_card)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_post_card, params_post_card)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row, strict=False)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to create a new card")
        return {"count": 0, "cards": []}
    else:
        return {"count of added cards": cursor.rowcount, "cards added": rowdicts}


def del_card(del_card_title):
    query = "DELETE FROM cards WHERE title = %s RETURNING *"
    params = (del_card_title,)
    try:
        with get_cursor() as cursor:
            cursor.execute(query, params)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row, strict=False)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to delete the card")
        return {"count": 0, "cards": []}
    else:
        return {"count of deleted cards": cursor.rowcount, "cards deleted": rowdicts}


def update_card(card_title, board_name):
    query_board_id = "SELECT board_id FROM boards WHERE board_name = %s;"
    params_board_id = (board_name,)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_board_id, params_board_id)
            board_id = cursor.fetchone()[0]
    except Exception:
        logger.exception("Failed to get board_id by board_name")

    query_card_status = "SELECT status FROM cards WHERE board = %s AND title = %s"
    params_card_status = (board_id, card_title)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_card_status, params_card_status)
            status = cursor.fetchone()[0]
    except Exception:
        logger.exception("Failed to get card status")
    else:
        if status == 1 or status == 2:
            status += 1
        else:
            return "Task i already done"

    query_update = """
        UPDATE cards
        SET status = %s, last_updated_at = %s
        WHERE board = %s AND title = %s
        RETURNING *;
    """
    params_update = (status, datetime.datetime.now(), board_id, card_title)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_update, params_update)
    except Exception:
        logger.exception("Failed to update card")
        return "Failed to update card"

    query_card_select = """
        SELECT title, boards.board_name AS board, status_name AS status
        FROM cards
        INNER JOIN boards ON cards.board = boards.board_id
        INNER JOIN status ON cards.status = status.status_id
        WHERE board = %s AND title = %s;
    """
    params_card_select = (board_id, card_title)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_card_select, params_card_select)
            colnames = [desc[0] for desc in cursor.description]
            response = [dict(zip(colnames, row, strict=False)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to get updated card")
        return {"count": 0, "cards": []}
    else:
        return {"count of updated cards": cursor.rowcount, "cards updated": response}


def get_estimation_card(board_name, column_name, assignee):
    query_estimation = """
        SELECT estimation FROM cards
        WHERE assignee = (SELECT user_id FROM users WHERE user_name = %s)
        AND status = (SELECT status_id FROM status WHERE status_name = %s);
    """
    params_estimation = (assignee, column_name)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_estimation, params_estimation)
            list_of_tuples = cursor.fetchall()
    except Exception:
        logger.exception("Failed to get list of estimation")
    try:
        res = TimeCounter(list_of_tuples)
        final_estimation = res.final_estimation()
    except Exception:
        logger.exception("Error TimeCounter")

    query_card = """
        SELECT title, boards.board_name AS board, status_name AS status, description,
        user_name AS assignee, estimation, cards.created_at AS created_at, user_name AS created_by,
        cards.last_updated_at AS last_updated_at, user_name AS last_updated_by
        FROM cards
        INNER JOIN boards ON cards.board = boards.board_id
        INNER JOIN status ON cards.status = status.status_id
        INNER JOIN users ON cards.assignee = users.user_id
        WHERE boards.board_name = %s AND status_name = %s
        AND user_name = %s;
    """
    params_card = (board_name, column_name, assignee)
    try:
        with get_cursor() as cursor:
            cursor.execute(query_card, params_card)
            rows_count = cursor.rowcount
            colnames = [desc[0] for desc in cursor.description]
            cards_selected = [dict(zip(colnames, row, strict=False)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to get cards")
        return {"count": 0, "cards": []}
    else:
        response = {
            "board": board_name,
            "column": column_name,
            "assignee": assignee,
            "count": rows_count,
            "estimation": final_estimation,
            "cards": cards_selected,
        }
        return response
