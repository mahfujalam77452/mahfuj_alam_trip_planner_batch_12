from flask import request,make_response
from app.models.trip import Trip,TripStatus
from app.models.expense import Expense
from app.extensions import db
from app.schemas.trip_schema import TripCreateSchema,TripResponseSchema,TripUpdateSchema,ExpenseAddSchema,StatusChangeSchema
from marshmallow import ValidationError
from app.validations.trip import is_date_range_valid,is_expense_valid,is_valid_state_change
from app.services.trip import get_trips,get_trip_by_id,delete_trip_by_id,update_trip_by_id
from werkzeug.exceptions import NotFound,BadRequest,Conflict,InternalServerError
from sqlalchemy.exc import  SQLAlchemyError

def create_a_trip():

    data = request.get_json()

    schema = TripCreateSchema()

    response_schema = TripResponseSchema()

    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:

        raise BadRequest(error.messages)
        
    
    start_date = validated_data["start_date"]
    end_date = validated_data["end_date"]

    if not is_date_range_valid(start_date,end_date):

        raise BadReauest("start date should be the same date or previous date of end date")

        
    
   
    trip = Trip(
        destination=validated_data["destination"],
        start_date=validated_data["start_date"],
        end_date=validated_data["end_date"],
        budget=validated_data["budget"],
        max_travelers=validated_data["max_travelers"]
    )

    try:
        db.session.add(trip)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")
    


    
    


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

        raise NotFound("This trip is not found in the trip list")


    return {
        "success":True,
        "message":"Trip found successfully",
        "data":response_schema.dump(trip)
    },200



def update_trip(id):

    trip = get_trip_by_id(id)

    if trip is None:

        raise NotFound("This trip is not found in the trip list")

        

    if trip.status == TripStatus.COMPLETED:

        raise Conflict("can't edit a completed trip")
        

    

    data = request.get_json()

    schema = TripUpdateSchema()

    response_schema = TripResponseSchema()

    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:

        raise BadRequest(error.message)

        
    
    trip = update_trip_by_id(id,validated_data)

    

    return {
        "success":True,
        "message":"Trip Updated successfully",
        "data":response_schema.dump(trip)
    },200



def delete_trip(id):

    response_schema = TripResponseSchema()

    trip = delete_trip_by_id(id)

    if trip is None:

        raise NotFound("This trip is not found in the trip list")

    return {
        "success":True,
        "message":"Trip deleted successfully",
        "data":response_schema.dump(trip)
    },200

def add_expense(id):

    trip = get_trip_by_id(id)
    
    if trip is None:

        raise NotFound("This trip is not found in the trip list")

    if trip.status != TripStatus.PLANNED or trip.status != TripStatus.ONGOING:
        raise Conflict(f"adding expense is not allowed for {trip.status.value.lower()} trip")
        

    data = request.get_json()

    schema = ExpenseAddSchema()


    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:
        raise BadRequest(error.messages)

        

    if not is_expense_valid(trip.budget,trip.expenses + validated_data["amount"]):
        raise Conflict("Your expense is exceeding the total budget")
        

    expense = Expense(
        trip_id = id,
        title = validated_data['title'],
        amount = validated_data["amount"]
    )

    try:
        db.session.add(expense)
        trip.expenses = trip.expenses + validated_data["amount"]
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")

    


    return {
        "success":True,
        "message":"expense added sucessfully",
        "data":{
            "id":expense.id,
            "trip_id":expense.trip_id,
            "title":expense.title,
            "amount":expense.amount
        }
    },201

def get_summary(id):

    trip = get_trip_by_id(id)
    
    if trip is None:

        raise NotFound("This trip is not found in the trip list")

    return {
        "destination":trip.destination,
        "date_of_trip":trip.start_date,
        "current_travelers":trip.current_travelers,
        "available_seats":trip.max_travelers - trip.current_travelers,
        "total_expense":trip.expenses,
        "reamaining_budget":trip.budget-trip.expenses


    },200
    
    

    

def change_status(id):

    trip = get_trip_by_id(id)
    
    if trip is None:

        raise NotFound("This trip is not found in the trip list")

    data = request.get_json()

    schema = StatusChangeSchema()


    try:
        validated_data = schema.load(data)
    
    except ValidationError as error:

        raise BadRequest(error.messages)

    proposed_status = TripStatus(validated_data["status"])

    if not is_valid_state_change(trip.status,proposed_status):

        raise Conflict(f"Status can't be changed form {trip.status.value} to {proposed_status.value}")

    try:
        trip.status = proposed_status
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise InternalServerError("Database error occurred.")

    

    return {
        "success":True,
        "message":"status updated successfully"
    },200


    









