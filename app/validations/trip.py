from app.models.trip import Trip,TripStatus
from app.extensions import db

next_status = {
    TripStatus.PLANNED:[TripStatus.ONGOING,TripStatus.CENCELLED],
    TripStatus.ONGOING:[TripStatus.COMPLETED,TripStatus.CENCELLED],
}
#########################################################################################
# State change validation
#########################################################################################

def is_valid_state_change(current_status,new_status):
    return new_status in next_status.get(current_status,[])

#########################################################################################
# Date range validation
#########################################################################################

def is_date_range_valid(start_date,end_date):

    return start_date <= end_date

#########################################################################################
# Expense validation
#########################################################################################

def is_expense_valid(budget,proposed_amount):
    return proposed_amount <= budget





