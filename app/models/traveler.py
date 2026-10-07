from app.extensions import db

class Traveler(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(80),
        nullable=False
    )

    email = db.Column(
        db.String,
        nullable=False,
        unique=True

    )