from ..carts.models import Carts
from ..reviews.models import Reviews
from ..extensions import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.relationship("Tokens", backref="user", lazy=True, uselist=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    cart = db.relationship("Carts", backref="user", lazy=True, uselist=False, cascade="all, delete")
    reviews = db.relationship("Reviews", backref="user", lazy=True)
    password = db.Column(db.String, nullable=False)
    is_staff = db.Column(db.Boolean, default=False)


