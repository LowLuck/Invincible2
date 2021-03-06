from flask import Flask, redirect, jsonify, request
from flask import render_template
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_unauthorized
# from werkzeug import secure_filename
import os
import random
import requests

from data.reports import Reports
from data.users import User
from data.stash import Stash
from data.public import Public
from forms.RegisterForm import RegisterForm
from forms.LoginForm import LoginForm
from forms.UploadingForm import UploadingForm
from forms.RandimpForm import RandimpForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/data.db")


@app.route('/stash')
def stash():
    db_sess = db_session.create_session()
    s = []
    for dbdata in db_sess.query(Stash).filter(Stash.user_id == current_user.id):
        s.append(dbdata)
    return render_template('stash.html', datahtml=s)


@app.route('/pubstash')
def pubstash():
    db_sess = db_session.create_session()
    s = []
    for dbdata in db_sess.query(Public).filter(Public.show == True):
        s.append(dbdata)
    return render_template('pubstash.html', datahtml=s)


@app.route('/report/<ids>')
def report(ids):
    db_sess = db_session.create_session()
    data = db_sess.query(Public).filter(Public.id == ids).first()
    data.show = False
    Report = Reports(fileid=ids, filename=data.content)
    db_sess.add(Report)
    db_sess.commit()

    return render_template('reportcomp.html')


@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    db_sess = db_session.create_session()
    data = db_sess.query(Stash).filter(Stash.id == id,
                                       Stash.user_id == current_user.id).first()
    db_sess.delete(data)
    os.remove(f'static/{data.content}')
    db_sess.commit()
    return redirect('/stash')


@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = UploadingForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        data = db_sess.query(Stash).filter(Stash.id == id,
                                           Stash.user_id == current_user.id).first()
        if data:
            form.key.data = data.key
        else:
            return 'Error'
    if request.method == "POST":
        db_sess = db_session.create_session()
        data = db_sess.query(Stash).filter(Stash.id == id,
                                           Stash.user_id == current_user.id).first()
        if data:
            data.key = form.key.data
            db_sess.commit()
            return redirect('/stash')
        else:
            return 'Error'
    return render_template('Editor.html', form=form)


# if form.validate_on_submit():
#     db_sess = db_session.create_session()
#     data = db_sess.query(Stash).filter(Stash.id == id, Stash.user_id == current_user.id).first()
#     stash = Stash(
#         key=form.key.data)
#
#     db_sess.add(stash)
#     db_sess.commit()
#     return render_template('Upload.html')
# except Exception:
# return 'Error, it might happen because key isnt unique'
# return render_template('stash.html', form=UploadingForm)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/export/<user>/<key>')
def export(user, key):
    db_sess = db_session.create_session()
    username = db_sess.query(User).filter(User.name == user).first()
    exfil = db_sess.query(Stash).filter(Stash.key == key, Stash.user_id == username.id).first()
    return jsonify(exfil.content)


@app.route('/pubexport/<key>')
def pubexport(key):
    db_sess = db_session.create_session()
    exfil = db_sess.query(Public).filter(Public.key == key).first()
    return jsonify(exfil.content)


def imgsave(cond, filename, data):
    if cond:
        namefile = filename
        with open('static/' + str(filename) + '', 'wb') as fileutil:
            fileutil.write(data)
    else:
        namefile = str(random.randint(100, 999)) + str(filename)
        with open('static/' + namefile, 'wb') as fileutil:
            fileutil.write(data)
    return namefile


@app.route('/pubimport', methods=['GET', 'POST'])
def pubimport_():
    form = UploadingForm()
    if form.validate_on_submit():
        file = form.file.data
        # filename = secure_filename(file.filename)
        filename = file.filename
        filenames = os.listdir('static')
        data = file.read()
        namefile = imgsave(filename not in filenames, filename, data)

        try:
            db_sess = db_session.create_session()
            publ = Public(
                content=namefile,
                key=form.key.data)
            db_sess.add(publ)
            db_sess.commit()
            return render_template('Upload.html')
        except Exception:
            return 'Error, it might happen because key isnt unique'
    return render_template('Pubimport.html', form=form)


@app.route('/import', methods=['GET', 'POST'])
def import_():
    form = UploadingForm()
    if form.validate_on_submit():
        file = form.file.data
        # filename = secure_filename(file.filename)
        filename = file.filename
        filenames = os.listdir('static')
        data = file.read()
        namefile = imgsave(filename not in filenames, filename, data)

        try:
            db_sess = db_session.create_session()
            stash = Stash(
                content=namefile,
                user_id=current_user.id,
                key=form.key.data)

            db_sess.add(stash)
            db_sess.commit()
            return render_template('Upload.html')
        except Exception:
            return 'Error, it might happen because key isnt unique'
    return render_template('import.html', form=form)


@app.route('/randimport', methods=['GET', 'POST'])
def randimport():
    form = RandimpForm()
    if form.validate_on_submit():
        filenames = os.listdir('static')
        rp = requests.get("https://api.thecatapi.com/v1/images/search").json()
        answ = rp[0]['url']
        rp2 = requests.get(answ)
        namefile = random.randint(1000, 9999)
        while namefile in filenames:
            namefile = str(random.randint(1000, 9999)) + '.pnj'
        with open(f'static/{namefile}', 'wb') as file:
            file.write(rp2.content)
        try:
            db_sess = db_session.create_session()
            stash = Stash(
                content=namefile,
                user_id=current_user.id,
                key=form.key.data)

            db_sess.add(stash)
            db_sess.commit()
            return render_template('Upload.html')
        except Exception:
            return 'Error'
    return render_template('randimport.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="???????????? ???? ??????????????????")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="?????????? ???????????????????????? ?????? ????????")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='??????????????????????', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="???????????????????????? ?????????? ?????? ????????????",
                               form=form)
    return render_template('login.html', title='??????????????????????', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run()
