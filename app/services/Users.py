from ..models import db
import json
import datetime
from sqlalchemy import desc

def getAllUsers():
    try:
        sqlQuery = "SELECT * from users"
        result = db.session.execute(sqlQuery)
        print(result)
        temp = []
        for b in result:
            temp.append({'id': b.id, "name": b.name, "description": b.description, 'email': b.email, "location": b.location, 'userTag': b.userTag, 'tweetCount': b.tweetCount})
        return ({'error': False, 'isUsersFetched': True, 'users': temp})
    except Exception as err:
        print(err)
        return ({'error': True, 'errormsg': str(err), 'isUsersFetched': False})
