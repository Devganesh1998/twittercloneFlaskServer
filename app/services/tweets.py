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
        userdata.tweetCount = userdata.tweetCount + 1,
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
        sqlQuery = "SELECT t.id, t.title, t.description, t.likes, t.userId, t.createdAt, u.profileImgUrl, u.followersCount, u.followingCount, u.userTag from tweets AS t JOIN users AS u ON t.userId = u.id WHERE t.userId = ANY (SELECT parentId from followers WHERE follower = :followerId) OR t.userId = :followerId ORDER BY t.createdAt DESC LIMIT :offset, 20"
        arg = ({"followerId": followerData.id, 'offset': off})
        tweets = db.session.execute(sqlQuery, arg)
        print(tweets)
        temp = []
        for b in tweets:
            temp.append({"id": b.id, "userTag": b.userTag, "followingCount": b.followingCount, "followersCount": b.followersCount, "profileImgUrl": b.profileImgUrl, "title": b.title, "likes": b.likes, "createdAt": str(
                b.createdAt), "description": b.description, "userId": b.userId})
        return ({'error': False, 'isTweetFetched': True, 'tweets': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isTweetFetched': False, 'sampleFormat': {'page': 1, 'email': 'testmail'}})


def likeATweet(data):
    try:
        if data is None or data['tweetId'] is None or data['likedUserMail'] is None:
            return ({'error': True, 'errormsg': "Given payload didn't met the requirements", 'isTweetLiked': False, 'sampleFormat': {'tweetId': 1, 'likedUserMail': 'testmail@mail.com'}})

        sqlQuery = "INSERT INTO likes (tweetId, likedUserId) VALUES (:tweetId, (SELECT id from users WHERE email = :likedUserMail));"
        arg = ({"tweetId": data["tweetId"],
                'likedUserMail': data['likedUserMail']})
        db.session.execute(sqlQuery, arg)
        
        tweetData = Tweet.query.filter(Tweet.id == data["tweetId"]).first()
        tweetData.likes = tweetData.likes + 1,
        db.session.commit()

        return ({'error': False, 'isTweetLiked': True})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isTweetLiked': False, 'sampleFormat': {'tweetId': 1, 'likedUserMail': 'testmail@mail.com'}})


# SELECT id, name, location, userTag, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";


# SELECT id, name, location, userTag, CASE WHEN (SELECT) AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";

# SELECT id, name, location, userTag, CASE WHEN (SELECT id from followers where parentId = users.id AND follower = 3) > 0 THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";

# SELECT id, name, location, userTag, CASE WHEN 2 = ANY (SELECT follower from followers where parentId = users.id) THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "ashwin12";

# SELECT id, name, location, userTag, CASE WHEN (SELECT id FROM users WHERE email = "testmail") = ANY (SELECT follower from followers where parentId = users.id) THEN true ELSE false END AS isFollowing, age, email, password, mobile, tweetCount, followingCount, followersCount, joined, dob AS "Date of birth", description, profileImgUrl, posterImgUrl from users WHERE users.email != "testmail";
