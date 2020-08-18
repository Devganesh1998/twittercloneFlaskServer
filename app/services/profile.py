from ..models import db
import json
import datetime
from sqlalchemy import desc

def getUserTweets(userEmail):
    try:
        if userEmail is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isTweetFetched': False})
        sqlQuery = "SELECT * from tweets JOIN users ON users.id = tweets.userId WHERE users.email = :userEmail"
        arg = ({"userEmail":userEmail})
        result = db.session.execute(sqlQuery,arg)
        print(result)
        temp = []
        for b in result:
            temp.append({"title": b.title, "description": b.description, 'email': b.email, "userId": b.userId, 'likes': b.likes, 'createdAt': str(b.createdAt)})
        return ({'error': False, 'isTweetFetched': True, 'tweets': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isTweetFetched': False})

def getProfile(userEmail):
    try:
        if userEmail is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isProfileFetched': False})
        sqlQuery = "SELECT * from users WHERE users.email = :userEmail"
        arg = ({"userEmail":userEmail})
        result = db.session.execute(sqlQuery,arg)
        print(result)
        temp = []
        for b in result:
            temp.append({"id": b.id,"name": b.name,"location": b.location,"userTag": b.userTag,"age": b.age, "description": b.description, 'email': b.email, "mobile": b.mobile, 'tweetCount': b.tweetCount, 'followingCount': b.followingCount, 'followersCount': b.followersCount, 'joined': str(b.joined), 'dob': str(b.dob), "profileImgUrl": b.profileImgUrl, "posterImgUrl": b.posterImgUrl})
        return ({'error': False, 'isProfileFetched': True, 'profile': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isProfileFetched': False})
