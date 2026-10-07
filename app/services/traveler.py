from app.models.traveler import Traveler
from app.models.travel import Travel
from app.models.trip import Trip
from app.extensions import db

def register_traveler(name,email):

    traveler = db.session.execute(
        db.seclect(Traveler).where(Traveler.email == email)
    ).scalar_one_or_none()

    if traveler:
        return traveler.id

    traveler = Traveler(
        name = name,
        email = email
    )

    db.session.add(traveler)
    db.session.commit()

    return traveler.id

def get_traveler_trip_dates(travel_id):

    stmt = (
        db.select(Trip.start_date,Trip.end_date)
        .join(Travel,Travel.trip_id == Trip.id)
        .where(Travel.traveler_id == traveler_id)
    )

    result = db.session.execute(stmt)

    return result.all()

