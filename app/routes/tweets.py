from . import tweet
from flask import request
from ..services.tweets import addNewTweet, getAllTweet, likeATweet
import json


@tweet.route('/')
def tweets_home():
    return 'tweet home'


@tweet.route('/add', methods=['POST'])
def signin():
    data = request.get_json()
    res = addNewTweet(data)
    return json.dumps(res)


@tweet.route('/like', methods=['POST'])
def likeTweet():
    data = request.get_json()
    res = likeATweet(data)
    return json.dumps(res)


@tweet.route('/getall', methods=['POST'])
def getTweets():
    data = request.get_json()
    res = getAllTweet(data)
    return json.dumps(res)
