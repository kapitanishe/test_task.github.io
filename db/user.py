import psycopg2

from app.custom_errors import errors as custom_errors
from db.connection_manager import get_cursor
from db.structured_data.user import (
    DBUserGetRequest,
    DBUserGetResponse,
    DBUserRow,
    DBUserSignInRequest,
    DBUserSignInResponse,
    DBUserSignUpRequest,
    DBUserSignUpResponse,
)


def get_users(core_request: DBUserGetRequest) -> DBUserGetResponse:
    query = "SELECT user_id, user_name, admin FROM users ORDER BY user_id LIMIT %s OFFSET %s"
    params = (core_request.page_size, core_request.offset)
    with get_cursor() as cursor:
        cursor.execute(query, params)
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            raise custom_errors.RecordNotFoundError
        users = []
        for row in rows:
            user_data = dict(zip(column_names, row, strict=False))
            user = DBUserRow(**user_data)
            users.append(user)
        return DBUserGetResponse(users=users)


def sign_up_user(core_request: DBUserSignUpRequest) -> DBUserSignUpResponse | None:
    query = "INSERT INTO users (user_name, user_password, admin) VALUES (%s, %s, %s) RETURNING *;"
    params = (core_request.name, core_request.password, core_request.role)

    try:
        with get_cursor() as cursor:
            cursor.execute(query, params)
            column_names = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            if row is None:
                msg = "user_name is not unique"
                raise custom_errors.UniqueError(msg) from None
            new_user = dict(zip(column_names, row, strict=False))
    except psycopg2.errors.UniqueViolation as exc:
        raise custom_errors.UniqueError from exc
    return DBUserSignUpResponse(name=new_user["user_name"], role=new_user["admin"])


def sign_in_user(core_request: DBUserSignInRequest) -> DBUserSignInResponse | None:
    query = "SELECT * FROM users WHERE user_name = %s;"
    params = (core_request.user_name,)

    with get_cursor() as cursor:
        cursor.execute(query, params)
        column_names = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        if row is None:
            msg = "user_name is not found in users"
            raise custom_errors.UnauthorizedError(msg) from None
        user = dict(zip(column_names, row, strict=False))

    return DBUserSignInResponse(
        id_=user["user_id"], name=user["user_name"], password=user["user_password"], role=user["admin"]
    )
