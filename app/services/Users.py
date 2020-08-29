from ..models import db
import json
import jwt
from flask import request
import datetime
from sqlalchemy import desc

authKey = 'secret'


def getAllUsers():
    try:
        sqlQuery = "SELECT * from users"
        result = db.session.execute(sqlQuery)
        print(result)
        temp = []
        for b in result:
            temp.append({'id': b.id, "name": b.name, "description": b.description, 'email': b.email,
                         "location": b.location, 'userTag': b.userTag, 'tweetCount': b.tweetCount})
        return ({'error': False, 'isUsersFetched': True, 'users': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isUsersFetched': False})

def getUsersToExplore():
    try:
        signedEmail = request.cookies.get('signedEmail')
        signedEmailPayload = jwt.decode(
            signedEmail, authKey, algorithms=['HS256'])
        print("signedEmailPayload['email']           ", signedEmailPayload['email'])
        sqlQuery = 'SELECT id, name, location, userTag, CASE WHEN (SELECT id FROM users WHERE email = :userMail) = ANY (SELECT follower from followers where parentId = users.id) THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != :userMail;'
        args = {
            "userMail": signedEmailPayload['email']
        }
        result = db.session.execute(sqlQuery, args)
        print(result)
        temp = []
        for b in result:
            temp.append({"id": b.id,"name": b.name,"location": b.location, 'isFollowing': b.isFollowing,"userTag": b.userTag,"age": b.age, "description": b.description, 'email': b.email, "mobile": b.mobile, 'tweetCount': b.tweetCount, 'followingCount': b.followingCount, 'followersCount': b.followersCount, 'joined': str(b.joined), 'dob': str(b['Date of birth']), "profileImgUrl": b.profileImgUrl, "posterImgUrl": b.posterImgUrl})
        return ({'error': False, 'isUsersFetched': True, 'users': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isUsersFetched': False})
