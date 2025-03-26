from flask import jsonify, request
from loguru import logger

from app.core import user as core_user
from app.custom_errors import errors as custom_errors


def get_users():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    try:
        users = core_user.get_users(page, page_size)
    except custom_errors.UnauthorizedError:
        return "Authorization failed", 401
    except custom_errors.DataGetError:
        return "Failed to get users", 500
    except custom_errors.RecordNotFoundError:
        return "No users in DB", 404
    except Exception:
        logger.exception("Error get_users")
        return "Unknown error", 500
    return jsonify(users)


def sign_up_user():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    username = req_dict.get("user_name")
    password = req_dict.get("password")
    role = req_dict.get("role")
    try:
        response = core_user.sign_up_user(username, password, role)
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.RoleError:
        return "Role must be 'admin' or 'user'", 400
    except custom_errors.UniqueError:
        return "User name is not unique", 404
    except Exception:
        logger.exception("Error sign_up_user")
        return "Unknown error", 500
    else:
        return jsonify(response)


def sign_in_user():
    try:
        req_dict = request.json
    except Exception:
        logger.exception("Bad request")
        return "Bad request", 400

    username = req_dict.get("user_name")
    password = req_dict.get("password")
    try:
        response = core_user.sign_in_user(username, password)
    except custom_errors.DataValidationError:
        return "Input data is not valid", 400
    except custom_errors.RecordNotFoundError:
        return "User name is not found", 404
    except custom_errors.UnauthorizedError:
        return "Password is incorrect", 401
    except Exception:
        logger.exception("Error sign_in_user")
        return "Unknown error", 500
    else:
        return jsonify(response)
