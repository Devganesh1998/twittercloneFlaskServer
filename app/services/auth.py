from ..models import db
from ..models.user import User
import json
import jwt
import datetime
from flask import make_response, request

# from BackEnd.twittercloneFlaskServer.redisInstance import *

import redis

redisIns = redis.Redis(host='localhost', port=6379)

authKey = 'secret'


def register_user(data):
    try:
        if data is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isRegisterSuccess': False, 'sampleFormat': {'name': 'test', 'location': "testLocation", 'userTag': "test", "age": 12, 'email': 'testmail', 'password': 'testpassword', 'mobile': '9736276323', 'description': 'this is a test description', 'profileImgUrl': 'https://test.com', 'posterImgUrl': 'https://test.com'}})
        print(data)
        tempUser = User(
            name=data['name'],
            location=data['location'],
            userTag=data['userTag'],
            age=data['age'],
            email=data['email'],
            password=data['password'],
            mobile=data['mobile'],
            joined=datetime.datetime.now(),
            dob=datetime.datetime.now(),
            tweetCount=0,
            followingCount=0,
            followersCount=0,
            description=data['description'],
            profileImgUrl=data['profileImgUrl'],
            posterImgUrl=data['posterImgUrl']
        )
        db.session.add(tempUser)
        db.session.commit()
        expirationTime = 60 * 60 * 2
        auth_token = jwt.encode(
            {"email": data['email'], 'userTag': data['userTag']}, authKey)
        signedEmail = jwt.encode({'email': data['email']}, authKey)
        resp = make_response({'error': False, 'isRegisterSuccess': True, 'message': 'Registered Successfully',
                              'user': {'username': data['userTag'], 'email': data['email']}})
        resp.set_cookie('signedEmail', str(signedEmail), max_age=expirationTime * 1000)
        redisIns.setex(str(signedEmail), expirationTime, str(auth_token))
        return resp
    except Exception as err:
        print(err)
        return({'error': True, 'isRegisterSuccess': False, 'errormsg': str(err),
                'sampleFormat': {'name': 'test', 'location': "testLocation", 'userTag': "test", "age": 12, 'email': 'testmail', 'password': 'testpassword', 'mobile': '9736276323', 'description': 'this is a test description', 'profileImgUrl': 'https://test.com', 'posterImgUrl': 'https://test.com'}})


def login_user(credentials):
    try:
        email = credentials['email']
        password = credentials['password']
        results = User.query.filter(User.email == email).first()
        flag = 0
        username = ""
        if results != None:
            if password == results.password:
                username = results.userTag
                auth_token = jwt.encode(
                    {"email": email, 'userTag': username}, authKey)
                flag = 1

        if(flag == 1):
            expirationTime = 60 * 60 * 2
            signedEmail = jwt.encode({'email': email}, authKey)
            resp = make_response({'error': False, 'message': 'Login Successful',
                                  'isLoginSuccess': True, 'user': {'username': username, 'email': email}})
            resp.set_cookie('signedEmail', str(signedEmail), max_age=expirationTime * 1000)
            redisIns.setex(str(signedEmail), expirationTime, str(authKey))
            return resp
        else:
            return ({'error': True, 'errormsg': 'Incorrect Password', 'isLoginSuccess': False, 'sampleFormat': {'email': 'testmail', 'password': 'testpassword'}})
    except Exception as err:
        return ({'error': True, 'errormsg': str(err), 'isLoginSuccess': False, 'sampleFormat': {'email': 'testmail', 'password': 'testpassword'}})


def logout_user():
    try:
        signedEmail = request.cookies.get('signedEmail')
        # redisIns.DEL(signedEmail)
        resp = make_response({'isLogoutSuccess': True})
        resp.set_cookie('signedEmail', '', max_age=0)
        print(resp)
        return resp
    except Exception as err:
        return({'isLogoutSuccess': False, 'errormsg': str(err)})


def verifyAuth():
    try:
        signedEmail = request.cookies.get('signedEmail')
        if (redisIns.get(signedEmail)):
            return({'isAuthenticated': True})
    except Exception as err:
        return({'isAuthenticated': False, 'errormsg': str(err)})
