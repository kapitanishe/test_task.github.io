from flask import jsonify
from loguru import logger
from db import user


def get_users():
    try:
        users = user.get_users()
    except Exception:
        logger.exception("Error get_users")
        return "", 500
    else:
        return jsonify(users)