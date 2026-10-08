from flask import Blueprint
from app.controllers.traveler import add_traveler,delete_traveler

traveler_bp = Blueprint("traveler",__name__,url_prefix="/api/v1/trips")

# Add traveler
@traveler_bp.route("/<int:id>/travelers",methods=["POST"])
def add_a_traveler(id):
    return add_traveler(id)

# Delete Traveler
@traveler_bp.route("/<int:id>/travelers/<int:traveler_id>",methods=["DELETE"])
def delete_a_traveler(id,traveler_id):
    return delete_traveler(id,traveler_id)


