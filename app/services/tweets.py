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
        # sqlQuery = "SELECT * from tweets JOIN users ON users.id = tweets.userId (SELECT parentId from followers WHERE follower = :followerId)"
        # arg = ({"followerId":data['followerId']})
        # result = db.session.execute(sqlQuery,arg)
        if data is None:
            return ({'error': True, 'errormsg': "Given payload is empty", 'isTweetFetched': False, 'sampleFormat': {'title': 'test', 'description': 'this is a test description', 'email': 'testmail'}})
        print(data)
        page = 1
        if data['page'] is not None:
            page = data['page']
        off = 10 * (int(page) - 1)
        tweets = Tweet.query.join(User).order_by(desc(Tweet.createdAt)).offset(off).limit(20).all()
        print(tweets)
        temp = []
        for b in tweets:
            temp.append({"id": b.id, "title": b.title, "description": b.description, "userId": b.userId})
        return ({'error': False, 'isTweetFetched': True, 'tweets': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isTweetFetched': False, 'sampleFormat': {'title': 'test', 'description': 'this is a test description', 'email': 'testmail'}})
