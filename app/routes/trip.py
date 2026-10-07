from flask import Blueprint
from app.controllers.trip import create_a_trip,all_trips,get_trip,update_trip,delete_trip

trip_bp = Blueprint("trip",__name__,url_prefix="/api/v1/trips")

@trip_bp.route("",methods=["POST"])
def create_trip():
    return create_a_trip()


@trip_bp.route("")
def list_trip():
    return all_trips()



@trip_bp.route("/<int:id>")
def get_a_trip(id):
    return get_trip(id)



@trip_bp.route("/<int:id>",methods=["PUT"])
def update_a_trip(id):
    return update_trip(id)


@trip_bp.route("/<int:id>",methods=["DELETE"])
def delete_a_trip(id):
    return delete_trip(id)


@trip_bp.route("/<int:id>/status",methods=["POST"])
def update_status(id):
    return "trip created"

@trip_bp.route("/<int:id>/expenses",methods=["POST"])
def expense(id):
    return add_expense(id)

@trip_bp.route("/<int:id>summary")
def summary(id):
    return get_summary(id)



