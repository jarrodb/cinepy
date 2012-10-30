import datetime
import hashlib
import re
from mongokit import Document, ObjectId
from forms.user import USER_TYPES
from media import Media

class User(Document):
    __database__ = 'cinepy'
    __collection__ = 'user'

    structure = {
        'name': unicode,
        'email': unicode,
        'password': unicode,
        'usertype': int,

        # One movie per session
        'session': {
            'movie': unicode, #movie uuid
            'uuid': unicode,
            'file': unicode,
            'date': datetime.datetime,
            'time': float,
            },

        'limited': [unicode], # List of ID's Limited Viewers can view
    }

    validators = {
    }

    use_dot_notation = True

    required_fields = [
        'name',
        'email',
        'password',
        'usertype',
        ]
    default_values = {
        'usertype': 3,
        }

    indexes = [
        {'fields': ['email'], 'unique': True},
    ]

    def set_password(self, password):
        hash_password = hashlib.md5(password).hexdigest()
        self.password = unicode(hash_password)
        #self.save()

    def usertype_display(self):
        return self.choice_title_from_id(USER_TYPES, self.usertype)

    def choice_title_from_id(self, choices, cid):
        # structure ((id, choice), (id, choice))
        for i, c in choices:
            if isinstance(i, int):
                cid = int(cid)
            else:
                cid = str(cid)

            if i == cid:
                return c

    def choice_id_from_title(self, choices, title):
        # structure ((id, choice), (id, choice))
        for i, c in choices:
            if c.lower() == title.lower():
                return i

    def is_atleast(self, usertype):
        usertype_id = self.choice_id_from_title(USER_TYPES, usertype)
        return self.usertype <= int(usertype_id)

    @property
    def is_admin(self):
        return self.usertype == 1

