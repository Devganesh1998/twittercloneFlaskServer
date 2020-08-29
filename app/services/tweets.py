from ..models import db
from ..models.tweets import Tweet
from ..models.user import User
import json
import datetime
from sqlalchemy import desc

def addNewTweet(data):
    try:
        if data is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isTweetAdded': False, 'sampleFormat': {'title': 'test', 'description': 'this is a test description', 'email': 'testmail'}})
        print(data)
        result = User.query.filter(User.email == data['email']).first()
        temptweet = Tweet(
            title=data['title'],
            description=data['description'],
            likes=0,
            createdAt=datetime.datetime.now(),
            updatedAt=datetime.datetime.now(),
            userId=result.id
        )
        db.session.add(temptweet)
        db.session.commit()
        
        userdata = User.query.filter(User.id == result.id).first()    
        userdata.tweetCount=userdata.tweetCount + 1,
        db.session.commit()
        
        return ({'error': False, 'isTweetAdded': True, 'message': 'Tweet Added Successfully'})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isTweetAdded': False, 'sampleFormat': {'title': 'test', 'description': 'this is a test description', 'email': 'testmail'}})


def getAllTweet(data):
    try:
        if data is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isTweetFetched': False, 'sampleFormat': {'page': 1, 'email': 'testmail'}})
        page = 1
        if data['page'] is not None:
            page = data['page']
        off = 20 * (int(page) - 1)

        followerData = User.query.filter(User.email == data['email']).first()
        sqlQuery = "SELECT * from tweets WHERE tweets.userId = ANY (SELECT parentId from followers WHERE follower = :followerId) OR tweets.userId = :followerId ORDER BY tweets.createdAt DESC LIMIT :offset, 20"
        arg = ({"followerId":followerData.id, 'offset': off})
        tweets = db.session.execute(sqlQuery,arg)
        print(tweets)
        temp = []
        for b in tweets:
            temp.append({"id": b.id, "title": b.title, "likes": b.likes, "createdAt": str(b.createdAt), "description": b.description, "userId": b.userId})
        return ({'error': False, 'isTweetFetched': True, 'tweets': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isTweetFetched': False, 'sampleFormat': {'page': 1, 'email': 'testmail'}})


# SELECT id, name, location, userTag, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";



# SELECT id, name, location, userTag, CASE WHEN (SELECT) AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";

# SELECT id, name, location, userTag, CASE WHEN (SELECT id from followers where parentId = users.id AND follower = 3) > 0 THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";

# SELECT id, name, location, userTag, CASE WHEN 2 = ANY (SELECT follower from followers where parentId = users.id) THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";

# SELECT id, name, location, userTag, CASE WHEN (SELECT id FROM users WHERE email = "testmail") = ANY (SELECT follower from followers where parentId = users.id) THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "testmail";