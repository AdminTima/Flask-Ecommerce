import datetime

from ..extensions import db


class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    photo = db.Column(db.String, nullable=False)
    bought_times = db.Column(db.Integer, default=0)
    reviews = db.relationship(
        "Reviews",
        backref="product",
        cascade="all, delete",
        lazy="select"
    )
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"))
    cart_items = db.relationship(
        "CartItems",
        backref="product",
        cascade="all, delete",
        lazy=True
    )
    created = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
    )
    updated = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )




