from app.models.trip import Trip
from app.extensions import db

def get_trips():

    stmp = db.select(Trip)

    result = db.session.execute(stmp)

    data = result.scalars().all()
    
    return data


def get_trip_by_id(id):

    stmp = db.select(Trip).where(Trip.id == id)

    result = db.session.execute(stmp)

    data = result.scalar_one_or_none()

    return data

def delete_trip_by_id(id):

    stmp = db.select(Trip).where(Trip.id == id)

    result = db.session.execute(stmp)

    data = result.scalar_one_or_none()

    if data is None:
        return None
    
    db.session.delete(data)
    db.session.commit()

    return data

def update_trip_by_id(trip,validated_data):

    

    for key,value in validated_data.items():

        setattr(trip,key,value)

    db.session.commit()

    return trip



