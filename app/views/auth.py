from flask import render_template, flash, redirect, url_for, Blueprint, request, session
from app.forms.users import LoginForm, RegistrationForm
from app.models.users import User
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    title = 'Login'
    if current_user.is_authenticated:
        return redirect(url_for('coin.list_coins'))
    else:
        if request.method == 'GET':
            return render_template('auth/login.html', form=form)

        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user is None or check_password_hash(user.password, password) == False:
            connect = 'no'
            flash('Email ou mot de passe incorrect')
            return render_template('auth/login.html', form=form, titre=title, connect=connect,code=401)
        login_user(user)
        session['username'] = current_user.username
        return redirect(url_for('coin.list_coins'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    print("use:" ,user)
    if user:
        flash('cette adresse email existe déjà merci d\'utliser une autre')
        return redirect(url_for('auth.register'))
    if form.validate_on_submit():
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Vous êtes bien inscrit')
        return redirect(url_for('auth.login'))
    else:
        flash('Veuillez remplir tous les champs')
        return redirect(url_for('auth.register'))


@auth.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('coin.list_coins'))
