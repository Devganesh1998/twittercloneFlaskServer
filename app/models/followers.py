from . import db
from .user import User

class Follower(db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.Integer, primary_key=True)
    parentId = db.Column(db.Integer,db.ForeignKey(User.id), nullable=False)
    follower = db.Column(db.Integer,db.ForeignKey(User.id), nullable=False)
