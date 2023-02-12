from ..extensions import db


class Tokens(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


