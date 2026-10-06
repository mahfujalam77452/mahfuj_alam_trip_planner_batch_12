from flask import request,make_response
from app.models.trip import Trip
from app.extensions import db
from app.schemas.trip_schema import TripCreateSchema,TripResponseSchema
from marshmallow import ValidationError
from app.validations.trip import is_date_range_valid
from app.services.trip import get_trips,get_trip_by_id,delete_trip_by_id,update_trip_by_id

def create_a_trip():

    data = request.get_json()

    schema = TripCreateSchema()

    response_schema = TripResponseSchema()

    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:

        return {
            "error":"Invalid input",
            "message":error.messages
        },400
    
    start_date = validated_data["start_date"]
    end_date = validated_data["end_date"]

    if not is_date_range_valid(start_date,end_date):

        return {
            "error":"Invalid date range",
            "message":"start date should be the same date or previous date of end date"
        },400
    
   


    trip = Trip(
        destination=validated_data["destination"],
        start_date=validated_data["start_date"],
        end_date=validated_data["end_date"],
        budget=validated_data["budget"],
        max_travelers=validated_data["max_travelers"]
    )
    


    db.session.add(trip)
    db.session.commit()
    


    return {
        "success":True,
        "message":"Trip created successfully",
        "data":response_schema.dump(trip)
    },201


def all_trips():

    trips = get_trips()
    response_schema = TripResponseSchema()

    return {
        "count":len(trips),
        "success":True,
        "message":"Trips extracted successfully",
        "data":[response_schema.dump(trip) for trip in trips]
    },200

def get_trip(id):

    trip = get_trip_by_id(id)
    response_schema = TripResponseSchema()

    if trip is None:

        return {
            "error":"Trip not found",
            "message":"This trip is not found"
        },404

    return {
        "success":True,
        "message":"Trip found successfully",
        "data":response_schema.dump(trip)
    }



