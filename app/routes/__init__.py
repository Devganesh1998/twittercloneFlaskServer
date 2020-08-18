from flask import Blueprint


user = Blueprint('user', __name__)
tweet = Blueprint('tweet', __name__)
profile = Blueprint('profile', __name__)

from . import User 
from . import tweets 
from . import profiles 