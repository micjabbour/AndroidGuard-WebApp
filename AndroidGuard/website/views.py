from . import main
from flask import render_template, flash, url_for, request
from .. import login_manager, db
from ..models import User, Device, Location
from .forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
from werkzeug.exceptions import abort


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        u = User.get_by_username(username)
        if u is not None and u.check_password(password):
            login_user(u, remember_me)
            flash("logged in as '{}'".format(username))
            return redirect(url_for('.devices'))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@main.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User(username=username, password=password)
        db.session.add(u)
        db.session.commit()
        flash("Welcome '{}'! Please login".format(username))
        return redirect(request.args.get('next')
                        or url_for('.login'))
    return render_template('signup.html', form=form)


@main.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash("User '{}' signed out successfully.".format(username))
    return redirect(url_for('.index'))


@main.route('/devices')
@login_required
def devices():
    return redirect(url_for('.index'))


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
