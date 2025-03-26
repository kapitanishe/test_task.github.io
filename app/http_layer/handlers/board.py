from flask import jsonify, request
from loguru import logger

from app.core import board as core_board
from app.custom_errors import errors as custom_errors


def get_boards():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    try:
        boards = core_board.get_boards(page, page_size)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.DataGetError:
        return "Failed to get boards", 500
    except custom_errors.RecordNotFoundError:
        return "No boards in DB", 404
    except Exception:
        logger.exception("Error get_boards")
        return "Unknown error", 500
    return jsonify(boards)


def create_board():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    title = req_dict.get("title")
    try:
        response = core_board.create_board(title)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.UniqueError:
        return "Title is not unique", 404
    except Exception:
        logger.exception("Error post_board")
        return "Unknown error", 500
    else:
        return jsonify(response)


def del_board():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    title = req_dict.get("title")
    try:
        response = core_board.del_board(title)
    except custom_errors.RoleError:
        return "Not enough rights", 404
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.RecordNotFoundError:
        return "Title not found", 404
    except Exception:
        logger.exception("Error del_boards")
        return "Unknown error", 500
    else:
        return jsonify(response)
