from app.extensions import db
from app.models.trip import Trip
from sqlalchemy import event,text
from sqlalchemy import CheckConstraint

class Expense(db.Model):

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "trip.id",
            ondelete="CASCADE"
        ),
        nullable = False
    )

    title = db.Column(
        db.String,
        nullable = False
    )

    amount = db.Column(
        db.Integer,
        nullable=False
    )

    # expense amount should be greater then 0
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="check_expense_amount_positive"
        ),
        
    )




