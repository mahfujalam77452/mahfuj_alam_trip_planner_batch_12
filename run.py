from app import create_app
from app.extensions import db
from app.models.trip import Trip
from app.models.travel import Travel
from app.models.traveler import Traveler
from app.models.expense import Expense

app = create_app()




with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)