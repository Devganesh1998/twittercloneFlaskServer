from . import db
from .user import User

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text(4294000000))
    likes = db.Column(db.Integer)
    userId = db.Column(db.Integer,db.ForeignKey(User.id), nullable=False)
    createdAt = db.Column(db.DateTime())
    updatedAt = db.Column(db.DateTime())
