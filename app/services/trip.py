from app.models.trip import Trip
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest,InternalServerError

#########################################################################################
# Get all trips 
#########################################################################################

def get_trips():

    stmp = db.select(Trip)

    result = db.session.execute(stmp)

    data = result.scalars().all()
    
    return data

#########################################################################################
# Get a trip by id
#########################################################################################

def get_trip_by_id(id):
    

    stmp = db.select(Trip).where(Trip.id == id)

    result = db.session.execute(stmp)

    data = result.scalar_one_or_none()

    return data

#########################################################################################
# Delete a Trip by id
#########################################################################################

def delete_trip_by_id(id):

    
    stmp = db.select(Trip).where(Trip.id == id)

    result = db.session.execute(stmp)

    data = result.scalar_one_or_none()

    if data is None:
        return None
    
    try:
        db.session.delete(data)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")
    
    

    return data

#########################################################################################
# Update a trip by id
#########################################################################################

def update_trip_by_id(trip,validated_data):

    
    start_date = validated_data.get("start_date",trip.start_date)
    end_date = validated_data.get("end_date",trip.end_date)

    if end_date <= start_date :

        raise BadRequest("End date can't before start date")
    


    budget = validated_data.get("budget",trip.budget)
    expenses = trip.expenses

    

    if budget < expenses :

        raise BadRequest("budget can't be less then the expenses")

    
    max_travelers = validated_data.get("max_travelers",trip.max_travelers)
    current_travelers = trip.current_travelers

    

    if max_travelers < current_travelers :

        raise BadRequest("max_travelers can't be less then the current travelers")



    for key,value in validated_data.items():

        setattr(trip,key,value)
    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")
    

    return trip



