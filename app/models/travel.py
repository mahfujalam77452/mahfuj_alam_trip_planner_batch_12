from app.extensions import db
from app.models.trip import Trip

class Travel(db.Model):

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "trip.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    traveler_id = db.Column(
        db.Integer,
        primary_key=True
    )