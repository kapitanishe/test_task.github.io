from flask import jsonify, request
from loguru import logger

from app.http_layer.schemas.card import CardDel, CardEstimation, CardPost, CardPut
from db import card


def get_cards():
    try:
        cards = card.get_cards()
    except Exception:
        logger.exception("Error get_cards")
        return "Unknown error", 500
    return jsonify(cards)


def post_card():
    inputs = CardPost(request)
    if not inputs.validate():
        logger.error(f"Validation errors: {inputs.errors}")
        return jsonify({"errors": inputs.errors}), 400

    req_json = request.json
    title = req_json["title"]
    board = req_json["board"]
    description = req_json["description"]
    estimation = req_json["estimation"]

    try:
        response = card.post_card(title, board, description, estimation)
    except Exception:
        logger.exception("Error post_card")
        return "Unknown error", 500
    else:
        return jsonify(response)


def del_card():
    inputs = CardDel(request)
    if not inputs.validate():
        logger.error(f"Validation errors: {inputs.errors}")
        return jsonify({"errors": inputs.errors}), 400

    req_json = request.json
    title = req_json["title"]

    try:
        response = card.del_card(title)
    except Exception:
        logger.exception("Error del_cards")
        return "Unknown error", 500
    else:
        return jsonify(response)


def put_card():
    inputs = CardPut(request)
    if not inputs.validate():
        logger.error(f"Validation errors: {inputs.errors}")
        return jsonify({"errors": inputs.errors}), 400

    req_json = request.json
    title = req_json["title"]
    board = req_json["board"]

    try:
        response = card.update_card(title, board)
    except Exception:
        logger.exception("Error update_card")
        return "Unknown error", 500
    else:
        return jsonify(response)


def get_card_estimation():
    inputs = CardEstimation(request)
    if not inputs.validate():
        logger.error(f"Validation errors: {inputs.errors}")
        return jsonify({"errors": inputs.errors}), 400

    req_json = request.json
    board = req_json["board"]
    column = req_json["column"]
    assignee = req_json["assignee"]

    try:
        response = card.get_estimation_card(board, column, assignee)
    except Exception:
        logger.exception("Error get_estimation_card")
        return "Unknown error", 500
    else:
        return jsonify(response)
