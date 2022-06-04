import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from Auth.models import User
from flask_login import login_user, logout_user, login_required
from MainApp.appFactory import db

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST', 'GET'])
def login__post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Ваш аккаунт не найден, пройдите регистрацию')
    if not check_password_hash(user.password, password):
        flash('Проверьте правильность заполнения данных')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/registration')
def registration():
    return render_template('registration.html')


@auth.route('/registration', methods=['POST', 'GET'])
def registration__post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if request.form['password'] == request.form['password2']:
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Пользователь с таким Email уже существует')
            return redirect(url_for('auth.registration'))
        new_user = User(email=email, name=name, password=generate_password_hash(
            password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        db.session.close()
    else:
        flash('Пароли не совпадают')
        return redirect(url_for('auth.registration'))
    sendMessage()
    flash('Вы успешно зарегестрировались')
    return redirect(url_for('auth.login'))


def sendMessage():
    name = request.form.get('name')
    email = request.form.get('email')
    url = 'https://api.telegram.org/bot5336401318:AAHbjzmb3TqWPFf25dNPP1D5YQHpVwUzW0M/sendMessage'
    req = {'chat_id': '-1001779026771', 'text': 'Зарегестрирован новый пользователь' '\n'  'Email: ' + email + '\n' 'Имя: ' + name}
    requests.post(url, req)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
