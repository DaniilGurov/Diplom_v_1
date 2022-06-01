from MainApp.appFactory import db
from flask_login import UserMixin, current_user
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    second_name = db.Column(db.String(1000))


class Avto(db.Model):
    __tablename__ = 'avto'
    avto_id = db.Column(db.Integer, primary_key=True)
    car_make = db.Column(db.String(100))
    number = db.Column(db.String, unique=True)
    car_model = db.Column(db.String(100))
    id_driver = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    years = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)


class AvtoPhoto(db.Model):
    __tablename__ = 'avtoPhoto'
    photo_id = db.Column(db.Integer, primary_key=True)
    url_photo = db.Column(db.String(512))
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'))
