import datetime

import psycopg2

from app.custom_errors import errors as custom_errors
from db.connection_manager import get_cursor
from db.structured_data.card import (
    DBCardColumnRequest,
    DBCardColumnResponse,
    DBCardCreateRequest,
    DBCardCreateResponse,
    DBCardDeleteRequest,
    DBCardDeleteResponse,
    DBCardEstimationRequest,
    DBCardEstimationResponse,
    DBCardGetRequest,
    DBCardGetResponse,
    DBCardRow,
    DBCardUpdateRequest,
    DBCardUpdateResponse,
)


def get_cards(core_request: DBCardGetRequest) -> DBCardGetResponse:
    query = "SELECT * FROM cards ORDER BY card_id LIMIT %s OFFSET %s"
    params = (core_request.page_size, core_request.offset)
    with get_cursor() as cursor:
        cursor.execute(query, params)
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            raise custom_errors.RecordNotFoundError
        cards = []
        for row in rows:
            card_data = dict(zip(column_names, row, strict=False))
            card = DBCardRow(**card_data)
            cards.append(card)
        return DBCardGetResponse(cards=cards)


def create_card(core_request: DBCardCreateRequest) -> DBCardCreateResponse:
    query_board = "SELECT board_id FROM boards WHERE board_name = %s"
    params_board = (core_request.board,)
    with get_cursor() as cursor:
        cursor.execute(query_board, params_board)
        row = cursor.fetchone()
        if row is None:
            raise custom_errors.RecordNotFoundError
        board_id = row[0]

    query_create_card = """
        INSERT INTO cards (assignee, board, created_at, description, estimation, status, title)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """
    dt_now = datetime.datetime.now()
    params_create_card = (
        core_request.assignee,
        board_id,
        dt_now,
        core_request.description,
        core_request.estimation,
        1,
        core_request.title,
    )
    try:
        with get_cursor() as cursor:
            cursor.execute(query_create_card, params_create_card)
            column_names = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            if row is None:
                raise custom_errors.UniqueError
            new_card = dict(zip(column_names, row, strict=False))
    except psycopg2.errors.UniqueViolation as exc:
        raise custom_errors.UniqueError from exc

    return DBCardCreateResponse(
        id_=new_card["card_id"],
        assignee=new_card["assignee"],
        board=new_card["board"],
        title=new_card["title"],
        estimation=new_card["estimation"],
        status=new_card["status"],
        description=new_card["description"],
        created_at=str(new_card["created_at"]),
        last_updated_at=str(new_card["last_updated_at"]),
    )


def del_card(core_request: DBCardDeleteRequest) -> DBCardDeleteResponse:
    query = "DELETE FROM cards WHERE title = %s RETURNING *"
    params = (core_request.title,)
    with get_cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            raise custom_errors.RecordNotFoundError from None
        column_names = [desc[0] for desc in cursor.description]
        deleted_card = dict(zip(column_names, row, strict=False))

    return DBCardDeleteResponse(title=deleted_card["title"])


def update_card(core_request: DBCardUpdateRequest) -> DBCardUpdateResponse:
    query_board_id = "SELECT board_id FROM boards WHERE board_name = %s;"
    params_board_id = (core_request.board,)
    with get_cursor() as cursor:
        cursor.execute(query_board_id, params_board_id)
        row = cursor.fetchone()
        if row is None:
            raise custom_errors.BoardNotFoundError from None
        board_id = row[0]

    query_card_status = "SELECT status FROM cards WHERE board = %s AND title = %s"
    params_card_status = (board_id, core_request.title)

    with get_cursor() as cursor:
        cursor.execute(query_card_status, params_card_status)
        row = cursor.fetchone()
        if row is None:
            raise custom_errors.CardNotFoundError from None
        status = row[0]

    if status == 1 or status == 2:
        status += 1
    elif status == 3:
        raise custom_errors.StatusError

    query_update = """
        UPDATE cards
        SET status = %s, last_updated_at = %s
        WHERE board = %s AND title = %s
        RETURNING *;
    """
    params_update = (status, datetime.datetime.now(), board_id, core_request.title)
    with get_cursor() as cursor:
        cursor.execute(query_update, params_update)
        row = cursor.fetchone()
        if row is None:
            raise custom_errors.CardUpdateNotFoundError from None
        column_names = [desc[0] for desc in cursor.description]
        updated_card = dict(zip(column_names, row, strict=False))

    return DBCardUpdateResponse(
        id_=updated_card["card_id"],
        assignee=updated_card["assignee"],
        board=updated_card["board"],
        title=updated_card["title"],
        estimation=updated_card["estimation"],
        status=updated_card["status"],
        description=updated_card["description"],
        created_at=str(updated_card["created_at"]),
        last_updated_at=str(updated_card["last_updated_at"]),
    )


def get_estimation(core_request: DBCardEstimationRequest) -> list[DBCardEstimationResponse]:
    query_estimation = """
        SELECT estimation FROM cards
        WHERE assignee = (SELECT user_id FROM users WHERE user_name = %s)
        AND status = (SELECT status_id FROM status WHERE status_name = %s);
    """
    params_estimation = (core_request.assignee, core_request.status)
    with get_cursor() as cursor:
        cursor.execute(query_estimation, params_estimation)
        rows = cursor.fetchall()
        if not rows:
            raise custom_errors.StatusNotFoundError
        estimation = [DBCardEstimationResponse(estimation=row[0]) for row in rows]
        return estimation


def get_cards_by_column(core_request: DBCardColumnRequest) -> list[DBCardColumnResponse]:
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
    params_card = (core_request.board, core_request.status, core_request.assignee)
    with get_cursor() as cursor:
        cursor.execute(query_card, params_card)
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        if rows:
            cards = []
            for row in rows:
                card_data = dict(zip(column_names, row, strict=False))
                card = DBCardColumnResponse(**card_data)
                cards.append(card)
            return cards
        else:
            query_board = "SELECT board_name FROM boards WHERE board_name = %s;"
            params_board = (core_request.board,)
            cursor.execute(query_board, params_board)
            board = cursor.fetchone()
            if not board:
                raise custom_errors.BoardNotFoundError
            else:
                raise custom_errors.MatchNotFoundError
