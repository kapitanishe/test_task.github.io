import datetime

import psycopg2

from app.custom_errors import errors as custom_errors
from db.connection_manager import get_cursor
from db.structured_data.board import (
    DBBoardCreateRequest,
    DBBoardCreateResponse,
    DBBoardDeleteRequest,
    DBBoardDeleteResponse,
    DBBoardGetRequest,
    DBBoardGetResponse,
    DBBoardRow,
)


def get_boards(core_request: DBBoardGetRequest) -> DBBoardGetResponse | None:
    query = "SELECT * FROM boards ORDER BY board_id LIMIT %s OFFSET %s"
    params = (core_request.page_size, core_request.offset)
    with get_cursor() as cursor:
        cursor.execute(query, params)
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            raise custom_errors.RecordNotFoundError
        boards = []
        for row in rows:
            board_data = dict(zip(column_names, row, strict=False))
            board = DBBoardRow(**board_data)
            boards.append(board)
        return DBBoardGetResponse(boards=boards)


def create_board(core_request: DBBoardCreateRequest) -> DBBoardCreateResponse | None:
    dt_now = datetime.datetime.now()

    query = """
            INSERT INTO boards (board_name, created_at, last_updated_at, status_id, user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
    """
    params = (core_request.board_name, dt_now, dt_now, 1, core_request.user_id)

    try:
        with get_cursor() as cursor:
            cursor.execute(query, params)
            column_names = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            if row is None:
                raise custom_errors.UniqueError
            new_board = dict(zip(column_names, row, strict=False))
    except psycopg2.errors.UniqueViolation as exc:
        raise custom_errors.UniqueError from exc

    return DBBoardCreateResponse(
        board_name=new_board["board_name"],
        created_at=new_board["created_at"],
        last_updated_at=new_board["last_updated_at"],
        status_id=new_board["status_id"],
        user_id=new_board["user_id"],
    )


def del_board(core_request: DBBoardDeleteRequest) -> DBBoardDeleteResponse | None:
    query = "DELETE FROM boards WHERE board_name = %s RETURNING *"
    params = (core_request.board_name,)
    with get_cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            raise custom_errors.RecordNotFoundError
        column_names = [desc[0] for desc in cursor.description]
        deleted_board = dict(zip(column_names, row, strict=False))

    return DBBoardDeleteResponse(board_name=deleted_board["board_name"])
