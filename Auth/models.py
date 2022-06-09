from enum import unique
from sqlalchemy import true
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
    surname = db.Column(db.String(1000))
    patronymic_name = db.Column(db.String(1000))
    role_name = db.Column(db.String(512))
    user_photo = db.Column(db.String(512))


class Avto(db.Model):
    __tablename__ = 'avto'
    avto_id = db.Column(db.Integer, primary_key=True)
    car_make = db.Column(db.String(100))
    number = db.Column(db.String, unique=True)
    car_model = db.Column(db.String(100))
    id_driver = db.Column(db.Integer)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.partner_id'))
    mileage = db.Column(db.Integer)
    years = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)


class AvtoInsurance(db.Model):
    __tablename__ = 'avtoinsurance'
    insurance_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(1000))
    date_start = db.Column(db.DateTime, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, default=datetime.utcnow)
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'))


class AvtoComment(db.Model):
    __tablename__ = 'avtoComment'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    commentPhoto = db.Column(db.String(512))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'))


class AvtoPhoto(db.Model):
    __tablename__ = 'avtoPhoto'
    photo_id = db.Column(db.Integer, primary_key=True)
    url_photo = db.Column(db.String(512))
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Driver(db.Model):
    __tablename__ = 'driver'
    driver_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_name = db.Column(db.String(512), db.ForeignKey('users.role_name'))
    avto_id = db.Column(db.Integer, db.ForeignKey('avto.avto_id'), unique=True)
    email = db.Column(db.String(100), db.ForeignKey('users.name'))
    name = db.Column(db.String(1000), db.ForeignKey('users.email'))
    surname = db.Column(db.String(1000), db.ForeignKey('users.surname'))
    patronymic_name = db.Column(
        db.String(1000), db.ForeignKey('users.patronymic_name'))
    driving_licence = db.Column(db.Integer)
    passport = db.Column(db.Integer)
    registration_address = db.Column(db.String(1000))
    residential_address = db.Column(db.String(1000))
    driver_photo = db.Column(db.String(1000), db.ForeignKey('users.user_photo'))
    photo_passport = db.Column(db.String(1000))
    photo_VU = db.Column(db.String(1000))
    insurance_id = db.Column(db.Integer, db.ForeignKey('avtoinsurance.insurance_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Partner(db.Model):
    __tablename__ = 'partner'
    partner_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_name = db.Column(db.String(512), db.ForeignKey('users.role_name'))
    email = db.Column(db.String(100), db.ForeignKey('users.name'))
    name = db.Column(db.String(1000), db.ForeignKey('users.email'))
    surname = db.Column(db.String(1000), db.ForeignKey('users.surname'))
    patronymic_name = db.Column(db.String(1000), db.ForeignKey('users.patronymic_name'))
    passport = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
