from app.extensions import db
from sqlalchemy import CheckConstraint
from enum import Enum

#Allowed Status for a Trip
class TripStatus(Enum):
    PLANNED = "PLANNED"
    CANCELLED = "CANCELLED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"


class Trip(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    destination = db.Column(
        db.String(100),
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )
    end_date = db.Column(
        db.Date,
        nullable=False
    )
    budget = db.Column(
        db.Integer,
        nullable=False
    )

    max_travelers = db.Column(
        db.Integer,
        nullable=False
    )
    current_travelers= db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    expenses = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    status = db.Column(
        db.Enum(TripStatus),
        nullable=False,
        default=TripStatus.PLANNED
    )

    __table_args__ = (
        CheckConstraint(
            "max_travelers > 0",
            name="check_trip_capacity_positive"
        ),
        CheckConstraint(
            "budget > 0",
            name="check_trip_budget_positive"
        ),
        CheckConstraint(
            "start_date < end_date",
            name="check_trip_date_range"
        )
    )

