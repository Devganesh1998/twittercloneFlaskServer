from . import profile
from flask import request
from ..services.profile import getUserTweets, getProfile
import json


@profile.route('/getTweets', methods=['GET'])
def getTweets():
    userEmail = request.args.get('userEmail')
    res = getUserTweets(userEmail)
    return json.dumps(res)


@profile.route('/', methods=['GET'])
def getprofile():
    data = request.args.get('userEmail')
    res = getProfile(data)
    return json.dumps(res)

