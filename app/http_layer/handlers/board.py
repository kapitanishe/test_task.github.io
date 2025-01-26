from flask import jsonify, request
from loguru import logger

from app.http_layer.schemas.board import BoardDel, BoardPost
from db import board


def get_boards():
    try:
        boards = board.get_boards()
    except Exception:
        logger.exception("Error get_boards")
        return "Unknown error", 500
    else:
        return jsonify(boards)


def post_board():
    inputs = BoardPost(request)
    if not inputs.validate():
        logger.error(f"Validation errors: {inputs.errors}")
        return jsonify({"errors": inputs.errors}), 400

    req_json = request.json
    title = req_json["title"]
    user_id = req_json["user_id"]

    try:
        response = board.post_board(title, user_id)
    except Exception:
        logger.exception("Error post_board")
        return "Unknown error", 500
    else:
        return jsonify(response)


def del_board():
    inputs = BoardDel(request)
    if not inputs.validate():
        logger.error(f"Validation errors: {inputs.errors}")
        return jsonify({"errors": inputs.errors}), 400

    req_json = request.json
    title = req_json["title"]
    try:
        response = board.del_board(title)
    except Exception:
        logger.exception("Error del_boards")
        return "Unknown error", 500
    else:
        return jsonify(response)
