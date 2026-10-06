from app.models.trip import Trip
from app.extensions import db

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





