from flask import request,make_response

from app.models.trip import Trip,TripStatus
from app.models.travel import Travel
from app.models.traveler import Traveler

from app.extensions import db
from app.schemas.traveler_schema import TravelerCreateSchema
from marshmallow import ValidationError
from app.validations.traveler import is_trip_exist,is_traveler_already_exist,is_travel_seat_available,is_trip_date_range_overlap
from app.services.traveler import register_traveler,get_traveler_trip_dates,delete_traveler_by_trip_and_traveler_id
from werkzeug.exceptions import NotFound,BadRequest,Conflict,InternalServerError
from sqlalchemy.exc import  SQLAlchemyError

def add_traveler(id):

    trip = is_trip_exist(id)

    if trip is None:

        raise NotFound("This trip is not found in the trip list")

    
    if trip.status != TripStatus.PLANNED:
        raise Conflict(f"This Trip is {trip.status.value}")
        


    data = request.get_json()
    schema = TravelerCreateSchema()

    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:

        raise BadRequest(error.messages)
    

    name = validated_data["name"]
    email = validated_data["email"]

    traveler = register_traveler(name,email)

    if traveler.name != name:
        raise Conflict("This email is already registered with another name")
        

    traveler_id = traveler.id
    
    if is_traveler_already_exist(trip.id,traveler_id):
        raise Conflict("You are alrady in this Trip")

       
    
    if not is_travel_seat_available(trip):
        raise Conflict("This trip has reached its maximum traveler capacity")
        
    trip_date = {
        "start_date":trip.start_date,
        "end_date":trip.end_date
    } 
    
    exist_dates = get_traveler_trip_dates(traveler_id,trip.id)

    if is_trip_date_range_overlap(trip_date,exist_dates):

        raise Conflict("This trip date range is overlaping with your other trips")
        
    
    travel = Travel(
        trip_id = trip.id,
        traveler_id = traveler_id
    )
    try:
        db.session.add(travel)
        trip.current_travelers = trip.current_travelers + 1
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")
    

    
    return {
        "success":True,
        "message":"you are added in this trip successfully !",
        "data":{"id":traveler.id,"name":traveler.name,"email":traveler.email}
    },201

def delete_traveler(id,traveler_id):

    travel = delete_traveler_by_trip_and_traveler_id(id,traveler_id)

    if travel is None:

        raise NotFound("you are not in this trip list")

        

    return {
        "success":True,
        "message":"You are removed from this trip successfully",
        
    },200

    