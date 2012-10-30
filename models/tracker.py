import datetime
import hashlib
import re
from mongokit import Document, ObjectId
from user import User

class Tracker(Document):
    __database__ = 'cinepy'
    __collection__ = 'tracker'

    structure = {
        'ttype': int,
        'ipaddr': unicode,
        'userid': ObjectId,
        'user': User,
        'date': datetime.datetime,

    }

    validators = {
    }

    use_dot_notation = True
    use_autorefs = True

    default_values = {
        'date': datetime.datetime.utcnow,
        'ttype': 1,
        }

    indexes = [
    ]


class LoginTracker(Tracker):
    default_values = {
        'ttype': 2,
        }


class MediaTracker(Tracker):
    __database__ = 'cinepy'
    __collection__ = 'tracker'

    structure = {
        'media': {
            'title': unicode,
            'collection': unicode,
            'id': ObjectId,
            }
    }

    default_values = {
        'ttype': 1,
        }

