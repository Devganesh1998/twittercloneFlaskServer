from . import db
from .user import User
from .tweets import Tweet

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    tweetId = db.Column(db.Integer,db.ForeignKey(Tweet.id), nullable=False)
    likedUserId = db.Column(db.Integer,db.ForeignKey(User.id), nullable=False)
