from datetime import timedelta

import psycopg2
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from loguru import logger
from pydantic import ValidationError

from app.core.authorize import check_general_authorization
from app.core.schemas.user import UserGetSchema, UserSignInSchema, UserSignUpSchema
from app.core.structured_data.user import CoreUserSignInResponse, CoreUserSignUpResponse
from app.custom_errors import errors as custom_errors
from db import user as db_user
from db.structured_data.user import DBUserGetRequest, DBUserSignInRequest, DBUserSignUpRequest


def get_users(page: int, page_size: int):
    try:
        check_general_authorization()
    except Exception as exc:
        logger.error(f"Authorization failed: {str(exc)}")
        raise custom_errors.UnauthorizedError from exc

    try:
        validated_data = UserGetSchema(page=page, page_size=page_size)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    offset = (validated_data.page - 1) * validated_data.page_size

    msg = DBUserGetRequest(page_size=validated_data.page_size, offset=offset)
    try:
        response = db_user.get_users(msg)
    except psycopg2.Error as exc:
        raise custom_errors.DataGetError(str(exc)) from exc
    except custom_errors.RecordNotFoundError:
        logger.error("Failed to get users from DB")
        raise
    else:
        return response


def sign_up_user(user_name, password, role):
    try:
        validated_data = UserSignUpSchema(user_name=user_name, password=password, role=role)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    bcrypt = Bcrypt()
    hashed_password = bcrypt.generate_password_hash(validated_data.password).decode("utf-8")

    if validated_data.role == "admin":
        role_request = True
    elif validated_data.role == "user":
        role_request = False
    else:
        logger.error("Role must be 'admin' or 'user'")
        raise custom_errors.RoleError

    db_msg = DBUserSignUpRequest(name=validated_data.user_name, password=hashed_password, role=role_request)
    try:
        db_request = db_user.sign_up_user(db_msg)
    except custom_errors.UniqueError:
        logger.error(f"Attempt to add already existing user: {validated_data.user_name}")
        raise
    except Exception:
        logger.exception("Error sign_up_user")
        return "Unknown error"

    role_response = "admin" if db_request.role else "user"
    return CoreUserSignUpResponse(name=db_request.name, role=role_response)


def sign_in_user(user_name, password):
    try:
        validated_data = UserSignInSchema(user_name=user_name, password=password)
    except ValidationError as exc:
        logger.error("Input data is not valid")
        raise custom_errors.DataValidationError from exc

    db_msg = DBUserSignInRequest(user_name=validated_data.user_name)
    try:
        db_request = db_user.sign_in_user(db_msg)
    except custom_errors.UnauthorizedError:
        logger.error(f"User with user_name: {validated_data.user_name} is not found")
        raise

    bcrypt = Bcrypt()
    pass_checked = bcrypt.check_password_hash(db_request.password, validated_data.password)
    if not pass_checked:
        logger.error("Passwords do not match")
        raise custom_errors.UnauthorizedError

    role = "admin" if db_request.role else "user"
    access_token = create_access_token(
        identity=str(db_request.id_),
        expires_delta=timedelta(hours=24),
        additional_claims={"name": db_request.name, "role": role},
    )
    return CoreUserSignInResponse(id_=db_request.id_, name=db_request.name, token=access_token, role=role)
