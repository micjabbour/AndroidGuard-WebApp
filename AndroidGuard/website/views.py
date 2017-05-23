from . import main
from flask import render_template, flash, url_for, request, jsonify
from .. import login_manager, db
from ..models import User, Device, Location
from .forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
from flask_googlemaps import Map, icons
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
            #flash("logged in as '{}'".format(username))
            return redirect(url_for('.my_devices'))
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
def my_devices():
    devices = current_user.devices
    first_dev_lat = 0
    first_dev_lng = 0
    markers = []
    if devices.count()>0:
        first_dev_lat = str(current_user.devices[0].last_location.latitude)
        first_dev_lng = str(current_user.devices[0].last_location.longitude)
        markers = [(first_dev_lat, first_dev_lng)]
    google_map = Map(
        identifier="google_map",  # for DOM element
        varname="google_map",  # for JS object name
        style="height:500px;width:100%;margin:0;",
        streetview_control=False,
        lat=first_dev_lat,
        lng=first_dev_lng,
        markers=markers
    )
    return render_template('devices.html', devices=devices, google_map=google_map)


@main.route('/get_devs_locs')
def get_devices_locations():
    user_devices = current_user.devices
    result = dict(
        devices=[device.get_device_dict() for device in user_devices]
    )
    return jsonify(result)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
