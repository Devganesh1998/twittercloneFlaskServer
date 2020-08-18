from . import profile
from flask import request
from ..services.profile import getUserTweets, getProfile, followUser, unfollowUser
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

@profile.route('/follow', methods=['POST'])
def followUserholder():
    data = request.get_json()
    res = followUser(data)
    return json.dumps(res)

@profile.route('/unfollow', methods=['POST'])
def unfollowUserholder():
    data = request.get_json()
    res = unfollowUser(data)
    return json.dumps(res)

