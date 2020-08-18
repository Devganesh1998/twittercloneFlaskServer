from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    location = db.Column(db.String(200))
    userTag = db.Column(db.String(200), unique=True, nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    mobile = db.Column(db.String(14))
    tweetCount = db.Column(db.Integer)
    followingCount = db.Column(db.Integer)
    followersCount = db.Column(db.Integer)
    joined = db.Column(db.DateTime())
    dob = db.Column(db.DateTime())
    description = db.Column(db.Text(4294000000))
    profileImgUrl = db.Column(db.Text(42940000))
    posterImgUrl = db.Column(db.Text(42940000))
