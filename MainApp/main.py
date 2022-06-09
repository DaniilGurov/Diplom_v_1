import os
import requests
from Auth.models import AvtoPhoto, Avto, Partner, User, Driver, AvtoComment
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


@main.route('/profile')
@login_required
def profile():
    if current_user.role_name == 'driver':
        atributes = Driver.query.filter_by(id=current_user.id).first()
        return render_template('profile.html', name=current_user.name, atrbutes=atributes)
    if current_user.role_name == 'partner':
        atributes = Partner.query.filter_by(id=current_user.id).first()
        return render_template('profile.html', name=current_user.name, atrbutes=atributes)
    return render_template('profile.html', name=current_user.name)


@main.route('/car/<int:avto_id>')
@login_required
def car(avto_id):
    driver = Driver.query.all()
    avto = Avto.query.filter_by(avto_id=avto_id).first()
    avtocomment = AvtoComment.query.filter_by(avto_id=avto_id).first()
    current_driver = Driver.query.filter_by(avto_id=avto_id).first()
    avtophoto = AvtoPhoto.query.order_by(
        AvtoPhoto.photo_id.desc()).filter_by(avto_id=avto_id).all()
    avtophoto = {(i.photo_id, i.url_photo) for i in avtophoto}
    return render_template('car.html', AvtoPhoto=avtophoto, avto=avto, current_driver=current_driver, name=current_user.name, driver=driver, avtocomment=avtocomment)


@main.route('/carEdit/<int:avto_id>', methods=['GET', 'POST'])
def carEdit(avto_id):
    avto = Avto.query.get(avto_id)
    if request.method == "POST":
        if request.form['driver'] != 'pure':
            avto.mileage = request.form['mileage']
            avtoID = Driver.query.filter_by(avto_id=avto_id).first()
            if avtoID is not None and avtoID.driver_id != int(request.form['driver']):
                driverId = Avto.query.filter_by(
                    id_driver=avtoID.driver_id).first()
                driverId.id_driver = None
                avtoID.avto_id = None

            driv = Driver.query.get(int(request.form['driver']))
            if avto.id_driver == int(request.form['driver']):
                return 'Уже назначена'
            driv.avto_id = avto_id

            avto.id_driver = int(request.form['driver'])
            try:
                db.session.commit()
                flash('Назначен водитель')
                return redirect(url_for(f'main.car', avto=avto, avto_id=avto_id, driver=driver))
            except:
                return "При редактировании пользователя произошла ошибка"
        else:
            avtoID = Driver.query.filter_by(avto_id=avto_id).first()
            driverId = Avto.query.filter_by(id_driver=avtoID.driver_id).first()
            driverId.id_driver = None
            avtoID.avto_id = None
            db.session.commit()
            flash('Водитель откреплен')
            return redirect(url_for(f'main.car', avto=avto, avto_id=avto_id, driver=driver))
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


@main.route('/photoUser/<int:id>', methods=['GET', 'POST'])
@login_required
def photoUser(id):
    if request.method == 'POST':
        user = User.query.get(id)
        driver = Driver.query.filter_by(id=user.id).first()
        f = request.files['file']
        if not f.filename:
            flash('Выберете файл')
        if f.filename:
            f.filename = str(random.randint(10000, 1000000))
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            photo_url = 'static/photo/' + f.filename
            user.user_photo = photo_url.split('/', 1)[1]
            driver.driver_photo = user.user_photo
            db.session.commit()

    return redirect(url_for(f'main.user', user=user, id=user.id))


@main.route('/addAvtoComment/<int:avto_id>', methods=['GET', 'POST'])
def addAvtoComment(avto_id):
    if request.method == "POST":
        avto = Avto.query.get(avto_id)
        avtocomment = AvtoComment.query.filter_by(avto_id=avto.avto_id).first()
        f = request.files['file']
        comment = request.form['comment']
        if comment is not None:
            flash('Заполните все поля')
        if not f.filename:
            flash('Выберете файл')
        if f.filename:
            f.filename = str(random.randint(10000, 1000000))
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            photo_url = 'static/photo/' + f.filename
            comment_photo = photo_url.split('/', 1)[1]
            try:
                new_comment = AvtoComment(
                    comment=comment, commentPhoto=comment_photo, avto_id=avto.avto_id)
                db.session.add(new_comment)
                db.session.commit()
            except:
                flash('При добавление авто возникла ошибка')
        return redirect(url_for(f'main.car', avto=avto, avto_id=avto_id, avtocomment=avtocomment))


@main.route('/reDriver/<int:driver_id>', methods=['GET', 'POST'])
def reDriver(driver_id):
    driver = Driver.query.get(driver_id)
    if request.method == "POST":
        driver.name = request.form['name']
        driver.email = request.form['email']
        driver.surname = request.form['surname']
        driver.patronymic_name = request.form['patronymic_name']
        try:
            db.session.commit()
            return redirect(url_for(f'main.user', driver=driver, driver_id=driver_id))
        except:
            return redirect(url_for(f'main.driver_profile', driver=driver, driver_id=driver_id))


@main.route('/reUser/<int:id>', methods=['GET', 'POST'])
def reUser(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form['name']
        user.email = request.form['email']
        user.surname = request.form['surname']
        user.patronymic_name = request.form['patronymic_name']
        if not user.role_name:
            user.role_name = request.form['user_role']
            if request.form['user_role'] == 'driver':
                dr = Driver.query.filter_by(id=id).first()
                if dr:
                    flash('Водитель уже существует')
                else:
                    new_driver = Driver(
                        name=user.name, email=user.email, role_name=user.role_name, id=user.id, surname=user.surname,
                        patronymic_name=user.patronymic_name, driver_photo=user.user_photo)
                    db.session.add(new_driver)
            if request.form['user_role'] == 'partner':
                pr = Driver.query.filter_by(id=id).first()
                if pr:
                    flash('Партнер уже существует')
                else:
                    new_partner = Partner(
                        name=user.name, email=user.email, role_name=user.role_name, id=user.id, surname=user.surname,
                        patronymic_name=user.patronymic_name)
                    db.session.add(new_partner)
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

    avtophoto = [AvtoPhoto.query.filter_by(
        avto_id=avto_id.avto_id).first() for avto_id in avto]

    return render_template('avto.html', avto=avto, current_user=current_user, avtophoto=avtophoto)


@main.route('/driver')
@login_required
def driver():
    user = User.query.filter_by(role_name='driver').all()
    driver = Driver.query.all()
    return render_template('driver.html', driver=driver, current_user=current_user, user=user)


@main.route('/driver_profile/<int:driver_id>')
@login_required
def driver_profile(driver_id):
    driver = Driver.query.filter_by(driver_id=driver_id).first()
    avto = Avto.query.filter_by(avto_id=driver.avto_id).first()
    return render_template('driver_profile.html', driver=driver, user=user, driver_id=driver_id, avto=avto)


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


@main.route('/partners')
@login_required
def partners():
    return render_template('partner.html', name=current_user.name)


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
            photo_url = 'static/photo/' + f.filename
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
        c = [g[0] for g in abs.keys()]
        r = abs[c[0]]
        path = a + r"static/" + r
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
            'chat_id': '-1001779026771', 'text': 'Email:  ' + email + '\n' 'Телефон:  ' + phone}
        requests.post(url, req)
        flash('Ваши данные успешно отправлены')
    return redirect('/')
