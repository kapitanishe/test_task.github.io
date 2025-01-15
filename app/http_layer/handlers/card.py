from flask import jsonify, request
from loguru import logger
from db import card


def get_cards():
    try:
        cards = card.get_cards()
    except Exception:
        logger.exception("Error get_cards")
        return "Unknown error", 500
    return jsonify(cards)


def post_card():
    try:
        req_json = request.json
    except Exception:
        logger.exception("Can't get request from user")
    else:
        title = req_json["title"]
        board = req_json["board"]
        description = req_json["description"]
        estimation = req_json["estimation"]
        try:
            new_card = card.post_card(title, board, description, estimation)
        except Exception:
            logger.exception("Error post_card")
        else:
            return jsonify(new_card)


def del_card():
    try:
        req_json = request.json
    except Exception:
        logger.exception("Can't get request from user")
    else:
        if "title" not in req_json:
            return "title is required", 400
        title = req_json["title"]
        try:
            response = card.del_card(title)
        except Exception:
            logger.exception("Error del_cards")
            return "Unknown error", 500
        else:
            return jsonify(response)


def put_card():
    try:
        req_json = request.json
    except Exception:
        logger.exception("Can't get request from user")
    else:
        title = req_json["title"]
        board = req_json["board"]
        try:
            card_updated = card.update_card(title, board)
        except Exception:
            logger.exception("Error update_card")
            return "Unknown error", 500
        else:
            return jsonify(card_updated)


def get_card_estimation():
    try:
        req_json = request.json
    except Exception:
        logger.exception("Can't get request from user")
    else:
        board = req_json["board"]
        column = req_json["column"]
        assignee = req_json["assignee"]

    try:
        cards_by_column = card.get_estimation_card(board, column, assignee)
    except Exception:
        logger.exception("Error get_estimation_card")
        return "Unknown error", 500
    else:
        return jsonify(cards_by_column)