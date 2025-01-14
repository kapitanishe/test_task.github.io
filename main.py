from flask import Flask, jsonify, request
from loguru import logger
from db import user, board, card

app = Flask(__name__)


@app.route("/user/list", methods=["GET"])
def get_users():
    try:
        users = user.get_users()
    except Exception:
        logger.exception("Error get_users")
        return "", 500
    else:
        return jsonify(users)


@app.route("/boards", methods=["GET"])
def get_boards():
    try:
        boards = board.get_boards()
    except Exception as exc:
        logger.exception("Error get_boards")
        return "Unknown error", 500
    else:
        return jsonify(boards)


@app.route("/board/create", methods=["POST"])
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


@app.route("/board/delete", methods=["DELETE"])
def del_boards():
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


@app.route("/cards", methods=["GET"])
def get_cards():
    # Простой, но грязный пример
    # limit = int(request.args.get("limit"))
    # if limit > 1000:
    #     return "The limit is expected to be between 1 and 1000", 400

    try:
        cards = card.get_cards()
    except Exception:
        logger.exception("Error get_cards")
        return "Unknown error", 500
    return jsonify(cards)


@app.route("/card/create", methods=["POST"])
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


@app.route("/card/delete", methods=["DELETE"])
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


@app.route("/card/update", methods=["PUT"])
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


@app.route("/report/cards_by_column", methods=["GET"])
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


# Run the Flask app on port 7000
if __name__ == "__main__":
    app.run(port=7000)
