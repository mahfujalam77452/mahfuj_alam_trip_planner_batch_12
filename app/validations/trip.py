from app.models.trip import Trip,TripStatus
from app.extensions import db

next_status = {
    TripStatus.PLANNED:[TripStatus.ONGOING,TripStatus.CENCELLED],
    TripStatus.ONGOING:[TripStatus.COMPLETED,TripStatus.CENCELLED],
}

def is_valid_state_change(current_status,new_status):
    return new_status in next_status.get(current_status,[])

def is_date_range_valid(start_date,end_date):

    return start_date <= end_date

# def is_date_range_overlap(start_date,end_date):

#     stmp = db.select(Trip).where(
#         (
#             Trip.end_date > start_date,
#             Trip.start_date < end_date
#         )
#     )
    

#     results = db.session.execute(stmp).scalars().all()

#     return len(results) > 0

def is_expense_valid(budget,proposed_amount):
    return proposed_amount <= budget





