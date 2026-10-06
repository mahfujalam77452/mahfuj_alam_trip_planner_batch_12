import os

class Config:
    # if run.sh 
    SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False