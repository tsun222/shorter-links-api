from flask import Blueprint, request, jsonify
from flask.typing import ResponseReturnValue

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import Url
from . import utils
import validators

api_bp = Blueprint("api", __name__)



@api_bp.route("/")
def index():
    return jsonify({"message": "Shorter Links API is up!"})



@api_bp.route("/shorten", methods=["POST"])
def shorten_url()-> ResponseReturnValue:
    data = request.get_json(silent=True) or {}
    input_url = data.get("url")

    if not isinstance(input_url, str) or not validators.url(input_url):
        return error_response(400, "invalid_input", "Invalid url input")
    
    max_attempts = 5
    short_code = None

    for _ in range(max_attempts):
        short_code_temp = utils.generate_random_url_code(8)
        try:
            with db.session.begin():
                row = Url(url=input_url, short_code=short_code_temp)
                db.session.add(row)
            short_code = short_code_temp
            break
        except IntegrityError as e:
            pass

    if short_code is None:
        return error_response(409, "code_conflict", "Failed to find a unique code")
    
    row = db.session.execute(sa.select(Url).where(Url.short_code == short_code)).scalar_one()
    return jsonify(row.to_dict()), 201



@api_bp.route("/shorten/<code>", methods=["GET"])
def retrieve_url(code: str) -> ResponseReturnValue:
    if not utils.is_valid_code(code):
        return error_response(400, "invalid_input", "Invalid url code")

    row = db.session.execute(sa.select(Url).where(Url.short_code == code)).scalar_one_or_none()
    if row is None:
        return error_response(404, "not_found", "Failed to find url corresponding to url code")
    
    return jsonify(row.to_dict()), 200



@api_bp.route("/shorten/<code>", methods=["PUT"])
def update_url(code: str) -> ResponseReturnValue:
    if not utils.is_valid_code(code):
        return error_response(400, "invalid_input", "Invalid url code")
    
    row = db.session.execute(sa.select(Url).where(Url.short_code == code)).scalar_one_or_none()
    if row is None:
        return error_response(404, "not_found", "Failed to find url corresponding to url code")
    
    data = request.get_json(silent=True) or {}
    input_url = data.get("url")
    if not isinstance(input_url, str) or not validators.url(input_url):
        return error_response(400, "invalid_input", "Invalid url input")
    
    row.url = input_url
    db.session.commit()
    return jsonify(row.to_dict()), 200



@api_bp.route("/shorten/<code>", methods=["DELETE"])
def delete_url(code: str) -> ResponseReturnValue:
    if not utils.is_valid_code(code):
        return error_response(400, "invalid_input", "Invalid url code")

    row = db.session.execute(sa.select(Url).where(Url.short_code == code)).scalar_one_or_none()
    if row is None:
        return error_response(404, "not_found", "Failed to find url corresponding to url code")
    
    db.session.delete(row)
    db.session.commit()
    return "", 204



@api_bp.route("/shorten/<code>/stats", methods=["GET"])
def get_statistics(code: str) -> ResponseReturnValue:
    if not utils.is_valid_code(code):
        return error_response(400, "invalid_input", "Invalid url code")

    row = db.session.execute(sa.select(Url).where(Url.short_code == code)).scalar_one_or_none()
    if row is None:
        return error_response(404, "not_found", "Failed to find url corresponding to url code")
    
    return jsonify(row.to_dict_with_statistics()), 200



def error_response(status: int, error: str, message: str) -> ResponseReturnValue:
    return jsonify({"error": error, "message": message}), status