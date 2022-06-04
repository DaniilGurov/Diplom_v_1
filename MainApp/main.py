import os
import requests
from Auth.models import AvtoPhoto, Avto, User, Driver
from MainApp.appFactory import db, UPLOAD_FOLDER
from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
import random


main = Blueprint('main', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html', current_user=current_user)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/car/<int:avto_id>')
@login_required
def car(avto_id):
    driver = Driver.query.all()
    avto = Avto.query.filter_by(avto_id=avto_id).first()
    avtophoto = AvtoPhoto.query.order_by(
        AvtoPhoto.photo_id.desc()).filter_by(avto_id=avto_id).all()
    avtophoto = {(i.photo_id, i.url_photo.replace(
        'static', '')[1:]) for i in avtophoto}
    return render_template('car.html', AvtoPhoto=avtophoto, avto=avto, name=current_user.name, driver=driver)


@main.route('/carEdit/<int:avto_id>', methods=['GET', 'POST'])
def carEdit(avto_id):
    avto = Avto.query.get(avto_id)
    if request.method == "POST":
        avto.car_make = request.form['car_make']
        try:
            db.session.commit()
            return redirect(url_for(f'main.car', avto=avto, avto_id=avto_id, driver=driver))
        except:
            return "При редактировании пользователя произошла ошибка"
    else:
        return redirect(url_for(f'main.car', avto=avto, avto_id=avto_id, driver=driver))


@main.route('/users')
def users():
    user = User.query.all()
    return render_template('users.html', user=user, current_user=current_user)


@main.route('/user/<int:id>')
def user(id):
    user = User.query.filter_by(id=id).all()
    return render_template('user.html', user=user, current_user=current_user, id=id)


@main.route('/reUser/<int:id>', methods=['GET', 'POST'])
def reUser(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form['name']
        user.email = request.form['email']
        user.role_name = request.form['user_role']
        try:
            db.session.commit()
            return redirect(url_for(f'main.user', user=user, id=id))
        except:
            return "При редактировании пользователя произошла ошибка"
    else:
        return redirect(url_for(f'main.user', user=user, id=id))


@main.route('/cars')
@login_required
def cars():
    avto = Avto.query.all()
    return render_template('avto.html', avto=avto, current_user=current_user)


@main.route('/driver')
@login_required
def driver():
    driver = Driver.query.all()
    return render_template('driver.html', driver=driver, current_user=current_user)


@main.route('/add_driver', methods=['GET', 'POST'])
@login_required
def addDriver():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        new_driver = Driver(name=name, email=email)
        try:
            db.session.add(new_driver)
            db.session.commit()
            db.session.close()
            return redirect(url_for('main.driver'))
        except:
            flash('Ошибка сохранения автомобиля')
    else:
        return redirect(url_for('main.driver'))


@main.route('/add_car', methods=['GET', 'POST'])
@login_required
def addCar():
    if request.method == 'POST':
        car_make = request.form['car_make']
        car_model = request.form['car_model']
        years = request.form['years']
        number = request.form['number']
        mileage = request.form['mileage']
        new_avto = Avto(car_make=car_make, car_model=car_model,
                        years=years, number=number, mileage=mileage)
        try:
            db.session.add(new_avto)
            db.session.commit()
            db.session.close()
            return redirect(url_for('main.cars'))
        except:
            flash('Ошибка сохранения автомобиля')
    else:
        return render_template('avto.html')


@main.route('/spare')
@login_required
def spare():
    return render_template('spare.html', name=current_user.name)


@main.route('/upload-photo', methods=['GET', 'POST'])
@login_required
def uploadPhoto():
    if request.method == 'POST':
        avto_id = request.args.get('avto_id')
        f = request.files['file']
        if not f.filename:
            flash('Выберете файл')
        if f.filename:
            f.filename = str(random.randint(10000, 1000000))
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            photo_url = UPLOAD_FOLDER + f.filename
            new_photo = AvtoPhoto(
                url_photo=photo_url.split('/', 1)[1], avto_id=avto_id)
            db.session.add(new_photo)
            db.session.commit()
            db.session.close()

    return redirect(url_for(f'main.car', avto_id=avto_id))


@main.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        avto_id = request.args.get('avto_id')
        a = r"C:/Users/gurovvaleriy/Desktop/pythonProject/MainApp/"
        abs = request.form
        c = [g[0]for g in abs.keys()]
        r = abs[c[0]]
        path = a+r"static/"+r
        path = path.replace('/', '\\')
        os.remove(path)
        AvtoPhoto.query.filter_by(photo_id=c[0]).delete()
        db.session.commit()
        db.session.close()
        return redirect(url_for(f'main.car', avto_id=avto_id))


@main.route('/telegram', methods=['POST', 'GET'])
def telegram():
    if request.method == 'POST':
        phone = request.form.get('phone')
        email = request.form.get('email')
        url = 'https://api.telegram.org/bot5336401318:AAHbjzmb3TqWPFf25dNPP1D5YQHpVwUzW0M/sendMessage'
        req = {
            'chat_id': '-1001779026771', 'text':  'Email:  ' + email + '\n' 'Телефон:  ' + phone}
        requests.post(url, req)
    return redirect('/')
