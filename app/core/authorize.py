from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.core.structured_data.user import TokenCheckResponse
from app.custom_errors import errors as custom_errors


def check_general_authorization():
    verify_jwt_in_request()


def check_token_and_return_data():
    verify_jwt_in_request()

    user_id = get_jwt_identity()
    jwt_data = get_jwt()
    name = jwt_data["name"]
    role = jwt_data["role"]

    return TokenCheckResponse(id=user_id, name=name, role=role)


def check_user_role():
    verify_jwt_in_request()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    if role != "admin":
        raise custom_errors.RoleError
