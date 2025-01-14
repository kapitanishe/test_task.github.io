import datetime
from db.connection_manager import get_cursor
from time_counter import TimeCounter
from loguru import logger


def get_cards():
    query = "SELECT * FROM cards"
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to fetch cards")
        return {"count": 0, "cards": []}
    else:
        return {"count": cursor.rowcount, "cards": rowdicts}


def post_card(new_card_name, new_card_board_name, new_card_description, new_card_estimation):
    dt_now = datetime.datetime.now()
    query_board_id = f"SELECT board_id FROM boards WHERE board_name = '{new_card_board_name}';"
    try:
        with get_cursor() as cursor:
            cursor.execute(query_board_id)
            board_id = cursor.fetchone()[0]
    except Exception:
        logger.exception("Failed to get board_id by board_name")
        return "Give a correct board name", 404  # TODO: написать класс ошибок
    query_post_card = f"""INSERT INTO cards (assignee, board, created_at, description, estimation, status, title)
                          VALUES (1, '{board_id}', '{dt_now}', '{new_card_description}', '{new_card_estimation}', 1, '{new_card_name}')
                          RETURNING *;"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query_post_card)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to create a new card")
        return {"count": 0, "cards": []}
    else:
        return {"count of added cards": cursor.rowcount, "cards added": rowdicts}


def del_card(del_card_title):
    query = f"DELETE FROM cards WHERE title = '{del_card_title}' RETURNING *"
    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            colnames = [desc[0] for desc in cursor.description]
            rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception as exc:
        logger.exception("Failed to delete the card")
        return {"count": 0, "cards": []}
    else:
        return {"count of deleted cards": cursor.rowcount, "cards deleted": rowdicts}


def update_card(card_title, board_name):
    query_board_id = f"SELECT board_id FROM boards WHERE board_name = '{board_name}';"
    try:
        with get_cursor() as cursor:
            cursor.execute(query_board_id)
            board_id = cursor.fetchone()[0]
    except Exception:
        logger.exception("Failed to get board_id by board_name")

    query_card_status = f"SELECT status FROM cards WHERE board = '{board_id}' AND title = '{card_title}'"
    try:
        with get_cursor() as cursor:
            cursor.execute(query_card_status)
            status = cursor.fetchone()[0]
    except Exception:
        logger.exception("Failed to get card status")
    else:
        if status == 1 or status == 2:
            status += 1
        else:
            return "Task i already done"

    query_update = f"""UPDATE cards 
                        SET status = '{status}', last_updated_at = '{datetime.datetime.now()}' 
                        WHERE board = '{board_id}' AND title = '{card_title}'
                        RETURNING *;"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query_update)
    except Exception:
        logger.exception("Failed to update card")
        return "Failed to update card"

    query_card_select = f"""SELECT title, boards.board_name AS board, status_name AS status   
                            FROM cards 
                            INNER JOIN boards ON cards.board = boards.board_id
                            INNER JOIN status ON cards.status = status.status_id
                            WHERE board = '{board_id}' AND title = '{card_title}';"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query_card_select)
            colnames = [desc[0] for desc in cursor.description]
            response = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except Exception:
        logger.exception("Failed to get updated card")
        return {"count": 0, "cards": []}
    else:
        return {"count of updated cards": cursor.rowcount, "cards updated": response}


def get_estimation_card(board_name_in_query, column_name_in_query, assignee_in_query):
    query_estimation = f"""SELECT estimation FROM cards 
                           WHERE assignee = (SELECT user_id FROM users WHERE user_name = '{assignee_in_query}') AND
                           status = (SELECT status_id FROM status WHERE status_name = '{column_name_in_query}');"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query_estimation)
            list_of_tuples = cursor.fetchall()
    except Exception:
        logger.exception("Failed to get list of estimation")
    try:
        res = TimeCounter(list_of_tuples)
        final_estimation = res.final_estimation()
    except Exception:
        logger.exception("Error TimeCounter")

    query_card = f"""SELECT title, boards.board_name AS board, status_name AS status, description, 
                        user_name AS assignee, estimation, cards.created_at AS created_at, user_name AS created_by,
                        cards.last_updated_at AS last_updated_at, user_name AS last_updated_by
                        FROM cards 
                        INNER JOIN boards ON cards.board = boards.board_id
                        INNER JOIN status ON cards.status = status.status_id
                        INNER JOIN users ON cards.assignee = users.user_id
                        WHERE boards.board_name = '{board_name_in_query}' AND status_name = '{column_name_in_query}' AND 
                        user_name = '{assignee_in_query}';"""
    try:
        with get_cursor() as cursor:
            cursor.execute(query_card)
            rows_count = cursor.rowcount
            colnames = [desc[0] for desc in cursor.description]
            cards_selected = [dict(zip(colnames, row)) for row in cursor.fetchall()]

    except Exception:
        logger.exception("Failed to get cards")
        return {"count": 0, "cards": []}
    else:
        response = dict(board=board_name_in_query, column=column_name_in_query, assignee=assignee_in_query,
                        count=rows_count, estimation=final_estimation, cards=cards_selected)
        return response
