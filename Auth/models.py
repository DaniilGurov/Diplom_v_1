from MainApp.appFactory import db
from flask_login import UserMixin, current_user
from datetime import datetime


class User(db.Model, UserMixin):
    @property
    def admin(self):
        return True if self.role_name == 'admin' else False

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    second_name = db.Column(db.String(1000))
    role_name = db.Column(db.String(512))


class Avto(db.Model):
    __tablename__ = 'avto'
    avto_id = db.Column(db.Integer, primary_key=True)
    car_make = db.Column(db.String(100))
    number = db.Column(db.String, unique=True)
    car_model = db.Column(db.String(100))
    id_driver = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    years = db.Column(db.Integer)


class AvtoPhoto(db.Model):
    __tablename__ = 'avtoPhoto'
    photo_id = db.Column(db.Integer, primary_key=True)
    url_photo = db.Column(db.String(512))
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'))


class Driver(db.Model):
    __tablename__ = 'driver'
    driver_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_name = db.Column(db.String(512), db.ForeignKey('users.role_name'))
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'))
    email = db.Column(db.String(100), db.ForeignKey('users.name'))
    name = db.Column(db.String(1000), db.ForeignKey('users.email'))
