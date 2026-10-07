from app.extensions import db
from app.models.travel import Travel
from app.services.trip import get_trip_by_id

def is_trip_exist(id):

    return get_trip_by_id(id)



def is_traveler_already_exist(id,traveler_id):

    travel = db.session.execute(
        db.select(Travel).where(
            Travel.trip_id==id,
            Travel.traveler_id ==traveler_id
        )
    ).scalar_one_or_none()

    if travel:
        return True
    
    return False

def is_travel_seat_available(trip):

    return (trip.current_travelers + 1) <= trip.max_travelers


def is_trip_date_range_overlap(trip_date,exist_dates):

    for date in exist_dates:

        if date.end_date > trip_date["start_date"] and date.start_date < trip_date["end_date"]:
            return True
        
    return False
     
