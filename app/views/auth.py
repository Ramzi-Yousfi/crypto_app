from flask import render_template, flash, redirect, url_for, Blueprint, request, session
from app.forms.users import LoginForm, RegistrationForm
from app.models.users import User
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import re # for regex
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login function is used to connect the user with his account.
    It checks if the email and password are corrects, then it logins him in.
    :return: The template auth/login
    """
    form = LoginForm()
    title = 'Login'
    if current_user.is_authenticated:
        return redirect(url_for('coin.list_coins'))
    else:
        if request.method == 'GET':
            return render_template('auth/login.html', form=form)
        email = request.form.get('email').lower()
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
    """
    The register function allows the user to register in the database.
    It takes as input a form and checks if it is valid. hash the password  ; it adds the new user to the database and redirects him/her
    to login page.
    :return: : request and redirect with or without error
    """
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    email = request.form.get('email').lower()
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('cette adresse email existe déjà !')
        return redirect(url_for('auth.register'))
    if form.validate_on_submit() and password == confirm_password and re.match(r"(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])", password):
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Vous êtes bien inscrit')
        return redirect(url_for('auth.login'))
    elif confirm_password != password:
        flash('les mots de passe ne correspondent pas')
        return redirect(url_for('auth.register'))
    elif re.match(r"(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])", password) == None:
        flash('le mot de passe doit contenir au moins 8 caractères et au moins une lettre majuscule, une lettre minuscule et un chiffre ')
        return redirect(url_for('auth.register'))
    else:
        flash('Veuillez remplir des informations valides')
        return redirect(url_for('auth.register'))


@auth.route('/logout')
@login_required
def logout():
    """
    The logout function logs the user out of their account and redirects them to the list_coins page.
    :return: A redirect to the list_coins view function
    """
    session.pop('username', None)
    logout_user()
    return redirect(url_for('coin.list_coins'))
