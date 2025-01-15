from flask import jsonify, request
from loguru import logger
from db import board


def get_boards():
    try:
        boards = board.get_boards()
    except Exception as exc:
        logger.exception("Error get_boards")
        return "Unknown error", 500
    else:
        return jsonify(boards)


def post_board():
    try:
        req_json = request.json
    except Exception:
        logger.exception("Error request post_boards")
    else:
        if not "title" in req_json:
            return "title is required", 400
        if not "user_id" in req_json:
            return "user_id is required", 400

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
    req_json = request.json
    if not "title" in req_json:
        return "title is required", 400
    title = req_json["title"]
    try:
        response = board.del_board(title)
    except Exception:
        logger.exception("Error del_boards")
        return "Unknown error", 500
    else:
        return jsonify(response)
