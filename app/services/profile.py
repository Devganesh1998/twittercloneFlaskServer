from ..models import db
import json
from ..models.followers import Follower
from ..models.user import User
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
            temp.append({"title": b.title, "description": b.description, 'userTag': b.userTag,'email': b.email, "userId": b.userId, 'likes': b.likes, 'profileImgUrl': b.profileImgUrl, 'followingCount': b.followingCount, 'followersCount': b.followersCount, 'createdAt': str(b.createdAt)})
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

def followUser(data):
    try:
        if data is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isProfileFollowed': False, 'sampleFormat': {'email': 'testmail', 'parentId': 2}})
        result = User.query.filter(User.email == data['email']).first()
        tempUser = Follower(
            parentId=data['parentId'],
            follower=result.id,
        )
        db.session.add(tempUser)
        db.session.commit()
        
        userdata = User.query.filter(User.id == result.id).first()    
        userdata.followingCount=userdata.followingCount + 1,
        db.session.commit()
        
        parentUserData = User.query.filter(User.id == data['parentId']).first()    
        parentUserData.followersCount=parentUserData.followersCount + 1,
        db.session.commit()
        return ({'error': False, 'isProfileFollowed': True, 'updatedProfile': {'id': parentUserData.id, 'name': parentUserData.name, 'location': parentUserData.location, 'userTag': parentUserData.userTag, 'age': parentUserData.age, 'email': parentUserData.email, 'password': parentUserData.password, 'mobile': parentUserData.mobile, 
                    'tweetCount': parentUserData.tweetCount, 'followingCount': parentUserData.followingCount, 'followersCount': parentUserData.followersCount, 'joined': str(parentUserData.joined), 'isFollowing': 1, 'dob': str(parentUserData.dob), 'description': parentUserData.description, 'profileImgUrl': parentUserData.profileImgUrl, 'posterImgUrl': parentUserData.posterImgUrl}})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isProfileFollowed': False, 'sampleFormat': {'email': 'testmail', 'parentId': 2}})

def unfollowUser(data):
    try:
        if data is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isProfileUnfollowed': False, 'sampleFormat': {'email': 'testmail', 'parentId': 2}})
        result = User.query.filter(User.email == data['email']).first()
        print('data', data)
        Follower.query.filter(Follower.parentId == data['parentId']).filter(Follower.follower == result.id).delete()
        db.session.commit()
        
        userdata = User.query.filter(User.id == result.id).first()    
        userdata.followingCount=userdata.followingCount - 1,
        db.session.commit()
        
        parentUserData = User.query.filter(User.id == data['parentId']).first()    
        parentUserData.followersCount=parentUserData.followersCount - 1,
        db.session.commit()
        return ({'error': False, 'isProfileUnfollowed': True})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isProfileUnfollowed': False, 'sampleFormat': {'email': 'testmail', 'parentId': 2}})
