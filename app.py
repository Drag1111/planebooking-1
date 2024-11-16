# app.py
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.attributes import flag_modified
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///flights.db')
app.config['SECRET_KEY'] = 'your_secret_key'

@app.template_filter('pretty_date')
def pretty_date(value):
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    day = date_obj.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return date_obj.strftime(f'%d{suffix} of %B %Y').lstrip('0') 


def load_user(user_id):
    return User.query.get(int(user_id))

from models import db, User, Flight, Reservation
from forms import RegisterForm, LoginForm
from flask import render_template
from datetime import datetime

def add_sample_flights():
    if not Flight.query.first(): 
        flights_data = [
            {"origin": "New York", "destination": "London", "date": "2024-12-15", "available_seats": ["1A", "1B", "1C", "1D", "2A", "2B"]},
            {"origin": "Paris", "destination": "Tokyo", "date": "2024-12-20", "available_seats": ["1A", "1B", "1C", "2A", "2B"]},
            {"origin": "Los Angeles", "destination": "Sydney", "date": "2024-12-25", "available_seats": ["1A", "1B", "2A", "2B", "3A"]},
            {"origin": "Dubai", "destination": "Moscow", "date": "2024-12-30", "available_seats": ["1A", "1B", "1C", "2A", "2B", "2C"]},
        ]
        for flight in flights_data:
            new_flight = Flight(
                origin=flight["origin"],
                destination=flight["destination"],
                date=flight["date"],
                available_seats=flight["available_seats"]
            )
            db.session.add(new_flight)
        db.session.commit()
        print("Sample flights added successfully!")
