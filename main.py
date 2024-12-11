from flask import Flask, jsonify, request
from loguru import logger
import database


app = Flask(__name__)


@app.route("/user/list", methods=["GET"])
def users_get_query():
    try:
        users = database.get_users()
    except Exception as exc:
        logger.exception("Не удалось получить список пользователей из функции get_users", exc)
    return jsonify(users)


@app.route("/boards", methods=["GET"])
def boards_get_query():
    try:
        boards = database.get_boards()
    except Exception as exc:
        logger.exception("Не удалось получить перечень досок из функции get_boards", exc)
    return jsonify(boards)


@app.route("/board/create", methods=["POST"])
def boards_post_query():
    try:
        req_json = request.json
    except Exception as exc:
        logger.exception("Не удалось получить запрос от пользователя", exc)

    if not "title" in req_json:
        return "title is required", 400
    if not "user_id" in req_json:
        return "user_id is required", 400

    title = req_json["title"]
    user_id = req_json["user_id"]
    try:
        rows_count = database.post_board(title, user_id)
    except Exception as exc:
        logger.exception("Не удалось добавить доску через функцию post_board", exc)
    return jsonify({"response": "Added " + str(rows_count) + " row"})


@app.route("/board/delete", methods=["DELETE"])
def boards_del_query():
    try:
        req_json = request.json
    except Exception as exc:
        logger.exception("Не удалось получить запрос от пользователя", exc)
    if not "title" in req_json:
        return "title is required", 400
    title = req_json["title"]
    try:
        rows_count = database.del_board(title)
    except Exception as exc:
        logger.exception("Не удалось удалить доску через функцию del_board", exc)
    return jsonify({"response": "Deleted " + str(rows_count) + " row"})


@app.route("/cards", methods=["GET"])
def cards_get_query():
    # Простой, но грязный пример
    limit = int(request.args.get("limit"))
    if limit > 1000:
        return "The limit is expected to be between 1 and 1000", 400
    try:
        cards = database.get_cards()
    except Exception as exc:
        logger.exception("Не удалось получить перечень карточек из функции get_cards", exc)
    return jsonify(cards)


@app.route("/card/create", methods=["POST"])
def cards_post_query():
    try:
        req_json = request.json
    except Exception as exc:
        logger.exception("Не удалось получить запрос от пользователя", exc)
    title = req_json["title"]
    board = req_json["board"]
    description = req_json["description"]
    estimation = req_json["estimation"]
    try:
        rows_count = database.post_card(title, board, description, estimation)
    except Exception as exc:
        logger.exception("Не удалось добавить карту через функцию post_card", exc)
    return jsonify({"response": "Added " + str(rows_count) + " row"})


@app.route("/card/delete", methods=["DELETE"])
def cards_del_query():
    try:
        req_json = request.json
    except Exception as exc:
        logger.exception("Не удалось получить запрос от пользователя", exc)
    if not "title" in req_json:
        return "title is required", 400
    title = req_json["title"]
    try:
        rows_count = database.del_card(title)
    except Exception as exc:
        logger.exception("Не удалось удалить карточку через функцию del_card", exc)
    return jsonify({"response": "Deleted " + str(rows_count) + " row"})


@app.route("/card/update", methods=["PUT"])
def cards_put_query():
    try:
        req_json = request.json
    except Exception as exc:
        logger.exception("Не удалось получить запрос от пользователя", exc)
    title = req_json["title"]
    board = req_json["board"]
    try:
        card_updated = database.update_card(title, board)
    except Exception as exc:
        logger.exception("Не удалось обновить карточку через функцию update_card", exc)
    return jsonify(card_updated)


@app.route("/report/cards_by_column", methods=["GET"])
def get_cards_by_column_query():
    try:
        req_json = request.json
    except Exception as exc:
        logger.exception("Не удалось получить запрос от пользователя", exc)
    board = req_json["board"]
    column = req_json["column"]
    assignee = req_json["assignee"]
    try:
        cards_by_column = database.get_cards_by_column(board, column, assignee)
    except Exception as exc:
        logger.exception("Не удалось получить отчет по колонке через функцию get_cards_by_column", exc)
    return jsonify(cards_by_column)

# Run the Flask app on port 7000
if __name__ == "__main__":
    app.run(port=7000)
