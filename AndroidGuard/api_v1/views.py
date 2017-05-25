from flask import request, jsonify, g, abort
from . import api_v1, creds_auth, token_auth
from ..models import User, Device, Location
from .. import db

# inspiration from https://blog.miguelgrinberg.com/post/restful-authentication-with-flask


@creds_auth.verify_password
def creds_verify(username, password):
    user = User.verify_credentials(username, password)
    if not user:
        return False
    g.user = user
    return True


@token_auth.verify_password
def token_verify(token, password):
    # password should be empty
    if password != "":
        return False
    # token should be a valid device token
    device = Device.verify_auth_token(token)
    if not device:
        return False
    g.device = device
    return True


@token_auth.error_handler
def token_error_handler():
    abort(401)


@creds_auth.error_handler
def creds_error_handler():
    abort(401)


# register new device and return a token for it
# if the device name already exists for this user,
# return a token for the already existing device
@api_v1.route('/devices', methods=["POST"])
@creds_auth.login_required
def register_device():
    try:
        device_name = request.get_json()['device_name']
    except TypeError:
        abort(400)
    device = Device.get_by_devicename(g.user, device_name)
    # if device does not exist, register it
    # else return the token for the already existing device
    already_exists = True
    if device is None:
        device = Device(name=device_name, user=g.user)
        db.session.add(device)
        db.session.commit()
        already_exists = False
    return jsonify(token=device.generate_auth_token(),
                   already_exists=already_exists)


# save new device's location in database
@api_v1.route('/locations', methods=["POST"])
@token_auth.login_required
def update_location():
    # insert new location into the database
    try:
        loc = Location(latitude=request.get_json()['latitude'],
                       longitude=request.get_json()['longitude'],
                       device=g.device)
    except TypeError:
        abort(400)
    db.session.add(loc)
    db.session.commit()
    return '', 204


@api_v1.route('/test_token', methods=["GET"])
@token_auth.login_required
def test_token():
    return '', 204


@api_v1.route('/test_creds', methods=["GET"])
@creds_auth.login_required
def test_creds():
    return '', 204


@api_v1.errorhandler(400)
def bad_request(e):
    return jsonify(error='bad request'), 400


@api_v1.errorhandler(403)
def forbidden(e):
    return jsonify(error='forbidden'), 403


@api_v1.errorhandler(401)
def not_authorized(e):
    return jsonify(error='authentication error'), 400


@api_v1.errorhandler(404)
def page_not_found(e):
    return jsonify(error='resource not found'), 404


@api_v1.errorhandler(500)
def server_error(e):
    return jsonify(error='server error'), 500


@api_v1.errorhandler(501)
def not_implemented(e):
    return jsonify(error='not implemented'), 501
