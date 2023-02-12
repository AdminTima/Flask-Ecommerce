from ..extensions import db


class Categories(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    products = db.relationship("Products", backref="category", lazy=True)


