from flask import Flask, request, jsonify, g, abort
from . import api_v1, auth
from ..models import User, Device, Location
from .. import db

# inspiration from https://blog.miguelgrinberg.com/post/restful-authentication-with-flask


# assumes that the username is a token first (when supplied an empty password)
# if it fails to authenticate, it tries authentication using a username/password
# when it authenticates using username/password pair:
#  g.auth_is_token is set to False
#  g.device is set to None
#  g.user is set to the authenticated user
# when it authenticates using a device token:
#  g.auth_is_token is set to True
#  g.device is set to the token's device
#  g.user is set to the device's user
@auth.verify_password
def verify_password(username_or_device_token, password):
    # first, try to authenticate by device token
    device = None
    if password == "":
        device = Device.verify_auth_token(username_or_device_token)
    if not device:
        # if it is not a token, try to authenticate by username
        user = User.verify_credentials(username_or_device_token, password)
        if not user:
            return False
        g.auth_is_token = False
        g.user = user
        g.device = None
        return True
    g.auth_is_token = True
    g.device = device
    g.user = device.user
    return True


@api_v1.route('/devices', methods=["POST"])
@auth.login_required
def register_device():
    # if user is being authenticated by device token
    if g.auth_is_token:
        # not allowed to register a new device
        abort(401)
    device_name = None
    try:
        device_name = request.get_json()['device_name']
    except TypeError:
        abort(400)
    device = Device.get_by_devicename(g.user, device_name)
    # if device does not exist, register it
    # else return the token for the already existing device
    if device is None:
        device = Device(name=device_name, user=g.user)
        db.session.add(device)
        db.session.commit()
    return jsonify(token=device.generate_auth_token())


@api_v1.route('/locations', methods=["POST"])
@auth.login_required
def update_location():
    # if not authenticated using a device token
    if not g.auth_is_token:
        abort(401)
    # insert new location into the database
    loc = Location(latitude=request.json.get('latitude'),
                   longitude=request.json.get('longitude'),
                   device=g.device)
    db.session.add(loc)
    db.session.commit()
    return '', 204


@api_v1.route('/test_token', methods=["GET"])
@auth.login_required
def test_token():
    # if not authenticated using a device token
    if not g.auth_is_token:
        abort(401)
    return '', 204


@api_v1.errorhandler(400)
def bad_request(e):
    return jsonify(error='bad request'), 400


@api_v1.errorhandler(403)
def forbidden(e):
    return jsonify(error='forbidden'), 403


@auth.error_handler
def auth_not_authorized():
    return jsonify(error='authentication error'), 401


@api_v1.errorhandler(401)
def not_authorized(e):
    return jsonify(error='not authorized'), 400


@api_v1.errorhandler(404)
def page_not_found(e):
    return jsonify(error='resource not found'), 404


@api_v1.errorhandler(500)
def server_error(e):
    return jsonify(error='server error'), 500


@api_v1.errorhandler(501)
def not_implemented(e):
    return jsonify(error='not implemented'), 501
