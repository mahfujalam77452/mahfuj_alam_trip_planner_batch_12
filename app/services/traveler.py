from app.models.traveler import Traveler
from app.models.travel import Travel
from app.models.trip import Trip
from app.extensions import db
from app.services.trip import get_trip_by_id

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

    db.session.add(traveler)
    db.session.commit()

    return traveler

def get_traveler_trip_dates(traveler_id,trip_id):

    stmt = (
        db.select(Trip.start_date,Trip.end_date)
        .join(Travel,Travel.trip_id == Trip.id)
        .where(Travel.traveler_id == traveler_id,Trip.id != trip_id)
    )

    result = db.session.execute(stmt)

    return result.all()

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
    
    db.session.delete(data)
    trip.current_travelers = trip.current_travelers - 1
    db.session.commit()

    return data


