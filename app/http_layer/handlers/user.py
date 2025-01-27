from flask import jsonify
from loguru import logger

from db import user as db_user
from app.core import user as core_user


def get_users():
    try:
        users = db_user.get_users()
    except Exception:
        logger.exception("Error get_users")
        return "", 500
    else:
        return jsonify(users)


def sign_up_user():  # TODO: реализовать
    # TODO: 1 реализация валидации
    core_user.sign_up_user()


def sign_in_user():  # TODO: реализовать
    # TODO: 1 реализация валидации
    core_user.sign_in_user()
