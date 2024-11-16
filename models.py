from app import db
from flask_login import UserMixin
import json
from sqlalchemy.types import TypeDecorator, TEXT

class JSONEncodedList(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value) 
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)  
        return value

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    available_seats = db.Column(JSONEncodedList, nullable=False)  
    reservations = db.relationship('Reservation', backref='flight_reservations', lazy=True) 

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    flight = db.relationship('Flight') 
