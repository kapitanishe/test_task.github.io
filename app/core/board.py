import psycopg2
from loguru import logger
from pydantic import ValidationError

from app.core.authorize import check_general_authorization, check_token_and_return_data, check_user_role
from app.core.schemas.board import BoardCreateSchema, BoardDeleteSchema, BoardGetSchema
from app.core.structured_data.board import CoreBoardCreateResponse, CoreBoardDeleteResponse
from app.custom_errors import errors as custom_errors
from db import board as db_board
from db.structured_data.board import DBBoardCreateRequest, DBBoardDeleteRequest, DBBoardGetRequest


def get_boards(page: int, page_size: int):
    try:
        check_general_authorization()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = BoardGetSchema(page=page, page_size=page_size)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    offset = (validated_data.page - 1) * validated_data.page_size

    msg = DBBoardGetRequest(page_size=validated_data.page_size, offset=offset)
    try:
        response = db_board.get_boards(msg)
    except psycopg2.Error as exc:
        raise custom_errors.DataGetError from exc
    except custom_errors.RecordNotFoundError:
        logger.error("Failed to get boards from DB")
        raise
    else:
        return response


def create_board(title: str):
    try:
        token_data = check_token_and_return_data()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = BoardCreateSchema(title=title, user_id=token_data.id)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_msg = DBBoardCreateRequest(board_name=validated_data.title, user_id=validated_data.user_id)
    try:
        db_request = db_board.create_board(db_msg)
    except custom_errors.UniqueError:
        logger.error(f"Attempt to create already existing board: {validated_data.title}")
        raise
    except Exception:
        logger.exception("Error post_board")
        return "Unknown error"
    else:
        return CoreBoardCreateResponse(
            board_name=db_request.board_name,
            created_at=db_request.created_at,
            last_updated_at=db_request.last_updated_at,
            status_id=db_request.status_id,
            user_id=db_request.user_id,
        )


def del_board(title: str):
    try:
        check_user_role()
    except custom_errors.RoleError:
        logger.error("User doesn't have enough rights")
        raise
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = BoardDeleteSchema(title=title)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_msg = DBBoardDeleteRequest(board_name=validated_data.title)
    try:
        db_request = db_board.del_board(db_msg)
    except psycopg2.Error as exc:
        raise custom_errors.DeletionError(str(exc)) from exc
    except custom_errors.RecordNotFoundError:
        logger.error(f"Attempt to delete non-existent board: {validated_data.title}")
        raise
    except Exception:
        logger.exception("Error post_board")
        return "Unknown error", 500
    else:
        return CoreBoardDeleteResponse(title=db_request.board_name)
