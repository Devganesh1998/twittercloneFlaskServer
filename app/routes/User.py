from . import user
from flask import request
from ..services.auth import register_user, login_user, logout_user, verifyAuth
import json


@user.route('/')
def users_home():
    return 'user home'


@user.route('/login', methods=['POST'])
def signin():
    credentials = request.get_json()
    res = login_user(credentials)
    return res


@user.route('/register', methods=['POST'])
def signup():
    data = request.get_json()
    res = register_user(data)
    return res


@user.route('/logout', methods=['GET'])
def logout():
    res = logout_user()
    return json.dumps(res)


@user.route('/verifyAuth', methods=['GET'])
def verifyAuthentication():
    res = verifyAuth()
    return json.dumps(res)
