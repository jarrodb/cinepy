import datetime
import hashlib
import re
from mongokit import Document, ObjectId
from user import User
from media import Media

class Queue(Document):
    __database__ = 'cinepy'
    __collection__ = 'queue'

    structure = {
        'user': User,
        'media': [Media],
        'date': datetime.datetime,
    }

    use_dot_notation = True

    indexes = [
    ]

