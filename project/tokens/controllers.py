from flask import Blueprint, request, jsonify
from .schemas import TokenSchema
from . import service


tokens_bp = Blueprint("tokens_bp", __name__, url_prefix="/tokens")


@tokens_bp.route("/refresh", methods=["POST"])
def refresh_tokens():
    request_data = TokenSchema().load(request.json)
    refresh_token = request_data["refresh"]
    tokens = service.get_new_tokens(refresh_token)
    return jsonify(tokens)









