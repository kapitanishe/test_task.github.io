from app.http_layer.handlers.board import create_board, del_board, get_boards
from app.http_layer.handlers.card import create_card, del_card, get_cards, get_cards_by_column, update_card
from app.http_layer.handlers.user import get_users, sign_in_user, sign_up_user


def register_routes(app):
    """
    Регистрирует маршруты в переданное приложение Flask.
    """
    app.add_url_rule("/user/list", "get_users", get_users, methods=["GET"])
    app.add_url_rule("/user/sign_up", "sign_up_user", sign_up_user, methods=["POST"])
    app.add_url_rule("/user/sign_in", "sign_in_user", sign_in_user, methods=["POST"])

    app.add_url_rule("/boards", "get_boards", get_boards, methods=["GET"])
    app.add_url_rule("/board/create", "post_board", create_board, methods=["POST"])
    app.add_url_rule("/board/delete", "del_boards", del_board, methods=["DELETE"])

    app.add_url_rule("/cards", "get_cards", get_cards, methods=["GET"])
    app.add_url_rule("/card/create", "create_card", create_card, methods=["POST"])
    app.add_url_rule("/card/delete", "del_card", del_card, methods=["DELETE"])
    app.add_url_rule("/card/update", "update_card", update_card, methods=["PUT"])
    app.add_url_rule("/report/cards_by_column", "get_cards_by_column", get_cards_by_column, methods=["GET"])
