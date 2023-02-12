from flask import Flask, send_from_directory
from .extensions import api, db
from .users.controllers import users_bp
from .db_config import db_url
from .tokens.controllers import tokens_bp
from .api_error import ApiError
from . import error_handlers
from jwt.exceptions import InvalidTokenError
from marshmallow.exceptions import ValidationError
from .reviews.controllers import reviews_bp
from flask_cors import CORS
from .carts.controllers import carts_bp

# Blueprints
from .carts.controllers import carts_bp
from .categories.controllers import categories_bp
from .products.controllers import products_bp
from .reviews.controllers import reviews_bp
from .tokens.controllers import tokens_bp
from .users.controllers import users_bp
from .auth.controllers import auth_bp


SQLALCHEMY_DATABASE_URI = db_url
UPLOAD_FOLDER = "/images"

app = Flask(__name__, static_url_path="")

CORS(app)

app.config.from_object(__name__)

# Registering blueprints
app.register_blueprint(carts_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(tokens_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

# Registering error handlers.
app.register_error_handler(ApiError, error_handlers.handle_api_error)
app.register_error_handler(InvalidTokenError, error_handlers.handle_token_error)
app.register_error_handler(ValidationError, error_handlers.handle_validation_error)

api.init_app(app)
db.init_app(app)


@app.route("/images/<path:path>")
def send_static(path):
    return send_from_directory("images", path)


if __name__ == "__main__":
    app.run()


