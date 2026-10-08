from app.models.traveler import Traveler
from app.models.travel import Travel
from app.models.trip import Trip
from app.extensions import db
from app.services.trip import get_trip_by_id
from sqlalchemy.exc import SQLAlchemyError

#########################################################################################
# Add name and email in Traveler table and Return the traveler if this email is not exist
# Just return the Traveler if already exist
#########################################################################################

def register_traveler(name,email):

    traveler = db.session.execute(
        db.select(Traveler).where(Traveler.email == email)
    ).scalar_one_or_none()

    if traveler:
        return traveler

    traveler = Traveler(
        name = name,
        email = email
    )

    try:
        db.session.add(traveler)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")

    

    return traveler

#########################################################################################
#Get all the trip dates the traveler in, expect the new trip where he want to travel
#########################################################################################

def get_traveler_trip_dates(traveler_id,trip_id):

    
    stmt = (
        db.select(Trip.start_date,Trip.end_date)
        .join(Travel,Travel.trip_id == Trip.id)
        .where(Travel.traveler_id == traveler_id,Trip.id != trip_id)
    )

    result = db.session.execute(stmt)

    return result.all()

#########################################################################################
# Delete Traveler by trip and traveler id
#########################################################################################

def delete_traveler_by_trip_and_traveler_id(trip_id,traveler_id):

    trip = get_trip_by_id(trip_id)

    if trip is None:
        return None
    
    

    stmp = db.select(Travel).where(Travel.trip_id == trip_id,
                                   Travel.traveler_id == traveler_id)

    result = db.session.execute(stmp)

    data = result.scalar_one_or_none()

    if data is None:
        return None

    try:
        db.session.delete(data)
        trip.current_travelers = trip.current_travelers - 1
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")
    
    

    return data


