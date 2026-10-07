from flask import request,make_response

from app.models.trip import Trip
from app.models.travel import Travel
from app.models.traveler import Traveler

from app.extensions import db
from app.schemas.traveler_schema import TravelerCreateSchema
from marshmallow import ValidationError
from app.validations.traveler import is_trip_exist,is_traveler_already_exist,is_travel_seat_available,is_trip_date_range_overlap
from app.services.traveler import register_traveler,get_traveler_trip_dates

def add_traveler(id):

    trip = is_trip_exist(id)

    if trip is None:
        return {
            "error":"Not Found",
            "message":"This Trip is not fount in the trip lists"
        },404

    data = request.get_json()
    schema = TravelerCreateSchema()

    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:

        return {
            "error":"Invalid input",
            "message":error.messages
        },400
    

    name = validated_data["name"]
    email = validated_data["email"]

    traveler_id = register_traveler(name,email)
    
    if is_traveler_already_exist(trip.id,traveler_id):

        return {
            "error":"Already exist",
            "message":"You are alrady in this Trip"
        },409
    
    if not is_travel_seat_available(trip):
        return {
            "error":"Trip Full",
            "message":"This trip has reached its maximum traveler capacity"
        },409

    trip_date = {
        "start_date":trip.start_date,
        "end_date":trip.end_date
    } 
    
    exist_dates = get_traveler_trip_dates(traveler_id,trip.id)

    if is_trip_date_range_overlap(trip_date,exist_dates):
        return {
            "error":"Date overlap",
            "message":"This trip date range is overlaping with your other trips"

        },409
    
    travel = Travel(
        trip_id = trip.id,
        traveler_id = traveler_id
    )

    db.session.add(travel)
    db.session.commit()
    
    return {
        "success":True,
        "message":"you are added in this trip successfully !"
    },201

def delete_traveler(id,traveler_id):
    return "traveler deleted"