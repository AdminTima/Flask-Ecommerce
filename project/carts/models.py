from ..extensions import db


class Carts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_sum = db.Column(db.Numeric, default=0, nullable=False)
    cart_items = db.relationship("CartItems", backref="carts", lazy="joined", cascade="all, delete")


class CartItems(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
    )
    amount = db.Column(db.Integer, default=1)
    total_sum = db.Column(db.Numeric, default=0, nullable=False)





