from app.http_layer.handlers.user import get_users
from app.http_layer.handlers.board import get_boards, post_board, del_board
from app.http_layer.handlers.card import get_cards, post_card, del_card, put_card, get_card_estimation


def register_routes(app):
    """
    Регистрирует маршруты в переданное приложение Flask.
    """
    app.add_url_rule("/user/list", "get_users", get_users, methods=["GET"])

    app.add_url_rule("/boards", "get_boards", get_boards, methods=["GET"])
    app.add_url_rule("/board/create", "post_board", post_board, methods=["POST"])
    app.add_url_rule("/board/delete", "del_boards", del_board, methods=["DELETE"])

    app.add_url_rule("/cards", "get_cards", get_cards, methods=["GET"])
    app.add_url_rule("/card/create", "post_card", post_card, methods=["POST"])
    app.add_url_rule("/card/delete", "del_card", del_card, methods=["DELETE"])
    app.add_url_rule("/card/update", "put_card", put_card, methods=["PUT"])
    app.add_url_rule("/report/cards_by_column", "get_card_estimation", get_card_estimation, methods=["GET"])
