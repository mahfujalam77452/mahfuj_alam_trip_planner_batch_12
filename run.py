from app import create_app


app = create_app()

@app.route("/helth")
def helth_check():
    return{
        "success":True,
        "message":"server helth is ok"
    },200

if __name__ == "__main__":
    app.run(debug=True)