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

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.template_filter('pretty_date')
def pretty_date(value):
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    day = date_obj.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return date_obj.strftime(f'%d{suffix} of %B %Y').lstrip('0') 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from models import db, User, Flight, Reservation
from forms import RegisterForm, LoginForm
from flask import render_template
from datetime import datetime


