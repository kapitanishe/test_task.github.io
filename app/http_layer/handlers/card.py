from flask import jsonify, request
from loguru import logger

from app.core import card as core_card
from app.custom_errors import errors as custom_errors


def get_cards():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    try:
        cards = core_card.get_cards(page, page_size)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataGetError:
        return "Failed to get cards", 500
    except custom_errors.RecordNotFoundError:
        return "No cards in DB", 404
    except Exception:
        logger.exception("Error get_cards")
        return "Unknown error", 500
    return jsonify(cards)


def create_card():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    title = req_dict.get("title")
    board = req_dict.get("board")
    description = req_dict.get("description")
    estimation = req_dict.get("estimation")

    try:
        response = core_card.create_card(title, board, description, estimation)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.UniqueError:
        return "Title is not unique", 404
    except Exception:
        logger.exception("Error create_card")
        return "Unknown error", 500
    else:
        return jsonify(response)


def del_card():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    title = req_dict.get("title")

    try:
        response = core_card.del_card(title)
    except custom_errors.RoleError:
        return "Not enough rights", 404
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.DeletionError:
        return "Card deletion failed", 500
    except custom_errors.RecordNotFoundError:
        return "Title not found", 404
    except Exception:
        logger.exception("Error del_card")
        return "Unknown error", 500
    else:
        return jsonify(response)


def update_card():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    title = req_dict.get("title")
    board = req_dict.get("board")

    try:
        response = core_card.update_card(title, board)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.UpdateError:
        return "Card update failed", 500
    except custom_errors.BoardNotFoundError:
        return "Board not found", 404
    except custom_errors.CardNotFoundError:
        return "Card not found", 404
    except custom_errors.StatusError:
        return "Card status is already Done", 400
    except custom_errors.CardUpdateNotFoundError:
        return "Updated card not found", 404
    except Exception:
        logger.exception("Error update_card")
        return "Unknown error", 500
    else:
        return jsonify(response)


def get_cards_by_column():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    board = req_dict.get("board")
    column = req_dict.get("column")

    try:
        response = core_card.get_cards_by_column(board, column)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.StatusNotFoundError:
        return "Card status not found", 404
    except custom_errors.EstimationCounterError:
        return "Estimation not counted", 404
    except custom_errors.BoardNotFoundError:
        return "Board not found", 404
    except custom_errors.MatchNotFoundError:
        return "No cards with necessary parameters", 404
    except Exception:
        logger.exception("Error get_cards_by_column")
        return "Unknown error", 500
    else:
        return jsonify(response)
