from tornado import escape
from tornado import web
from mongokit import ObjectId
from libs.torn.base import BaseHandler
from libs.torn.forms import TornadoMultiDict
from libs.models.pager import Paginator
from forms.movie import MovieSearchForm
import re


class MoviesImport(object):

    TITLE = '\xa9nam'
    DATE = '\xa9day'
    GENRES = '\xa9gen'
    ACTORS = '\xa9ART'
    LONGDESC = 'ldes'

    def __init__(self, filename):
        from mutagen.mp4 import MP4
        self._movie = MP4(filename)

    def __repr__(self):
        return '<Movie: %s>' % (self.title if self.title else '*Unknown*')

    @property
    def title(self):
        _title = self._movie.get(self.TITLE, None)
        if _title:
            return unicode(_title[0])
        return None

    @property
    def genres(self):
        _genres = self._movie.get(self.GENRES, None)
        if _genres:
            _genres = _genres[0].split(',')
            return [unicode(g.strip()) for g in _genres]
        return None

    @property
    def actors(self):
        _actors = self._movie.get(self.ACTORS, None)
        if _actors:
            _actors = _actors[0].split(',')
            return [unicode(name.strip()) for name in _actors]
        return None

    @property
    def date(self):
        from datetime import datetime
        _date = self._movie.get(self.DATE, None)
        if _date:
            _date = datetime.strptime(_date[0], '%Y-%m-%dT%H:%M:%SZ')
            return _date
        return None


class UsersHandler(BaseHandler):
    tpl = 'admin/user/users.html'

    @web.authenticated
    def get(self):
        users = self.conn.User.find().sort('name', -1).limit(30)
        self.render(self.tpl, **{
            'nav_active': 'admin',
            'users': users,
            })

