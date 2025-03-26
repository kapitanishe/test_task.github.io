import psycopg2
from loguru import logger
from pydantic import ValidationError

from app.core.authorize import check_general_authorization, check_token_and_return_data, check_user_role
from app.core.estimation_counter import EstimationCounter
from app.core.schemas.card import (
    CardColumnGetSchema,
    CardCreateSchema,
    CardDeleteSchema,
    CardGetSchema,
    CardUpdateSchema,
)
from app.core.structured_data.card import (
    CoreCardColumnResponse,
    CoreCardCreateResponse,
    CoreCardDeleteResponse,
    CoreCardUpdateResponse,
)
from app.custom_errors import errors as custom_errors
from db import card as db_card
from db.structured_data.card import (
    DBCardColumnRequest,
    DBCardCreateRequest,
    DBCardDeleteRequest,
    DBCardEstimationRequest,
    DBCardGetRequest,
    DBCardUpdateRequest,
)


def get_cards(page: int, page_size: int):
    try:
        check_general_authorization()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = CardGetSchema(page=page, page_size=page_size)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    offset = (validated_data.page - 1) * validated_data.page_size

    msg = DBCardGetRequest(page_size=validated_data.page_size, offset=offset)
    try:
        response = db_card.get_cards(msg)
    except psycopg2.Error as exc:
        raise custom_errors.DataGetError(str(exc)) from exc
    except custom_errors.RecordNotFoundError:
        logger.error("Failed to get cards from DB")
        raise
    else:
        return response


def get_cards_by_column(board: str, column: str):
    try:
        token_data = check_token_and_return_data()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = CardColumnGetSchema(board=board, column=column, assignee=token_data.name)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_estimation_msg = DBCardEstimationRequest(assignee=validated_data.assignee, status=validated_data.column)
    try:
        db_estimation_request = db_card.get_estimation(db_estimation_msg)
    except custom_errors.StatusNotFoundError:
        logger.error(f"Failed to get cards with status: '{validated_data.column}' to current user")
        raise

    try:
        result = EstimationCounter(db_estimation_request)
        sum_estimation = result.final_estimation()
    except Exception as exc:
        logger.error(f"Error EstimationCounter: {str(exc)}")
        raise custom_errors.EstimationCounterError from exc

    db_card_msg = DBCardColumnRequest(
        status=validated_data.column, board=validated_data.board, assignee=validated_data.assignee
    )
    try:
        db_card_request = db_card.get_cards_by_column(db_card_msg)
    except custom_errors.BoardNotFoundError:
        logger.error(f"Failed to get board: '{validated_data.board}'")
        raise
    except custom_errors.MatchNotFoundError:
        logger.error(f"No necessary cards found on board '{validated_data.board}'.")
        raise
    return CoreCardColumnResponse(
        board=validated_data.board,
        column=validated_data.column,
        assignee=validated_data.assignee,
        count=len(db_card_request),
        estimation=sum_estimation,
        cards=db_card_request,
    )


def create_card(title: str, board: str, description: str, estimation: str) -> CoreCardCreateResponse:
    try:
        token_data = check_token_and_return_data()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = CardCreateSchema(title=title, board=board, description=description, estimation=estimation)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_msg = DBCardCreateRequest(
        assignee=int(token_data.id),
        title=validated_data.title,
        board=validated_data.board,
        description=validated_data.description,
        estimation=validated_data.estimation,
    )
    try:
        db_request = db_card.create_card(db_msg)
    except custom_errors.RecordNotFoundError:
        logger.error(f"Failed to get board_id by board_name: {validated_data.board}")
        raise
    except custom_errors.UniqueError:
        logger.error(f"Attempt to create already existing card: {validated_data.title}")
        raise
    else:
        return CoreCardCreateResponse(
            id_=db_request.id_,
            assignee=db_request.assignee,
            board=db_request.board,
            title=db_request.title,
            estimation=db_request.estimation,
            status=db_request.status,
            description=db_request.description,
            created_at=db_request.created_at,
            last_updated_at=db_request.last_updated_at,
        )


def del_card(title: str):
    try:
        check_user_role()
    except custom_errors.RoleError:
        logger.error("User doesn't have enough rights")
        raise
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = CardDeleteSchema(title=title)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_msg = DBCardDeleteRequest(title=validated_data.title)
    try:
        db_request = db_card.del_card(db_msg)
    except psycopg2.Error as exc:
        raise custom_errors.DeletionError(str(exc)) from exc
    except custom_errors.RecordNotFoundError:
        logger.error(f"Attempt to delete non-existent card: {validated_data.title}")
        raise
    except Exception:
        logger.exception("Error del_card")
        return "Unknown error"
    else:
        return CoreCardDeleteResponse(title=db_request.title)


def update_card(title: str, board: str):
    try:
        check_general_authorization()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = CardUpdateSchema(title=title, board=board)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_msg = DBCardUpdateRequest(title=validated_data.title, board=validated_data.board)
    try:
        db_request = db_card.update_card(db_msg)
    except psycopg2.Error as exc:
        raise custom_errors.UpdateError(str(exc)) from exc
    except custom_errors.BoardNotFoundError:
        logger.error(f"Board not found: {validated_data.board}")
        raise
    except custom_errors.CardNotFoundError:
        logger.error(f"Card with name: '{validated_data.title}' not found on board: '{validated_data.board}'")
        raise
    except custom_errors.StatusError:
        logger.warning("Card status is Done")
        raise
    except custom_errors.CardUpdateNotFoundError:
        logger.error(f"Updated card with name: '{validated_data.title}' not found")
        raise
    except Exception:
        logger.exception("Error update_card")
        return "Unknown error"
    else:
        return CoreCardUpdateResponse(
            id_=db_request.id_,
            assignee=db_request.assignee,
            board=db_request.board,
            title=db_request.title,
            estimation=db_request.estimation,
            status=db_request.status,
            description=db_request.description,
            created_at=db_request.created_at,
            last_updated_at=db_request.last_updated_at,
        )
