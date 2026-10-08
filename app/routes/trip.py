from flask import Blueprint
from app.controllers.trip import create_a_trip,all_trips,get_trip,update_trip,delete_trip,add_expense,get_summary,change_status

trip_bp = Blueprint("trip",__name__,url_prefix="/api/v1/trips")

# Add a Trip
@trip_bp.route("",methods=["POST"])
def create_trip():
    return create_a_trip()

# Get all trips
@trip_bp.route("")
def list_trip():
    return all_trips()


# Get a trip by id 
@trip_bp.route("/<int:id>")
def get_a_trip(id):
    return get_trip(id)


# Update a Trip
@trip_bp.route("/<int:id>",methods=["PUT"])
def update_a_trip(id):
    return update_trip(id)

# Delete a Trip
@trip_bp.route("/<int:id>",methods=["DELETE"])
def delete_a_trip(id):
    return delete_trip(id)

# Change Status
@trip_bp.route("/<int:id>/status",methods=["PATCH"])
def update_status(id):
    return change_status(id)

# Add expense
@trip_bp.route("/<int:id>/expenses",methods=["POST"])
def expense(id):
    return add_expense(id)
    
#Get Summery
@trip_bp.route("/<int:id>/summary")
def summary(id):
    return get_summary(id)



