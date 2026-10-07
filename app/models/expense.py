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

__table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="check_expense_amount_positive"
        ),
        
    )

@event.listens_for(Expense.__table__,"after_create")

def create_expense_trigger(target,connection,**kwargs):
    connection.execute(
        text(
            """
            CREATE TRIGGER after_expense_insert
            AFTER INSERT ON expense
            FOR EACH ROW
            BEGIN
               UPDATE trip
               SET expenses = expenses + NEW.amount
               WHERE id = NEW.trip_id;
            END
            """
        )
    )