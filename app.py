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

def reset_database():
    with app.app_context(): 
        db.drop_all()  
        db.create_all()  
        add_sample_flights() 

reset_database()

@app.route('/')
def home():
    
    nearest_flights = Flight.query.filter(
        Flight.date >= datetime.now().strftime('%Y-%m-%d')
    ).order_by(Flight.date.asc()).limit(3).all()

    return render_template('home.html', flights=nearest_flights)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        flash('Registration successful! You are now logged in.')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/profile')
@login_required
def profile():
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', name=current_user.username, reservations=user_reservations)

@app.route('/flights')
@login_required
def flights():
    flights = Flight.query.all()
    return render_template('flights.html', flights=flights)


@app.route('/reserve/<int:flight_id>', methods=['POST'])
@login_required
def reserve(flight_id):
    seat_number = request.form['seat_number']
    flight = Flight.query.get_or_404(flight_id)
    
    existing_reservation = Reservation.query.filter_by(user_id=current_user.id, flight_id=flight_id).first()
    if existing_reservation:
        flash('You already have a reservation for this flight.')
        return redirect(url_for('flights'))

    if seat_number not in flight.available_seats:
        flash('Seat is not available. Please choose another seat.')
        return redirect(url_for('flights'))
    
    flight.available_seats.remove(seat_number)
    flag_modified(flight, "available_seats")  
    
    reservation = Reservation(user_id=current_user.id, flight_id=flight_id, seat_number=seat_number)
    db.session.add(reservation)
    
    db.session.commit()
    
    flash('Seat reserved successfully!')
    return redirect(url_for('profile'))



