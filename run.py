from app import create_app
from app.extensions import db
from app.models.trip import Trip

app = create_app()

@app.route("/helth")
def helth_check():
    return{
        "success":True,
        "message":"server helth is ok"
    },200


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)