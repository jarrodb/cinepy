from tornado import escape
from tornado import web
from uuid import uuid4
from mongokit import ObjectId
from libs.torn.base import ViewHandler, MovieBaseHandler
from libs.torn.forms import TornadoMultiDict
from libs.models.pager import Paginator
from libs.torn.decorators import user_passes
from forms.movie import MovieForm, MovieSearchForm, MoviePosterForm
from settings import settings
from datetime import datetime
import wtforms
import os
import re


class PlayerHandler(MovieBaseHandler):
    tpl = 'player/player.html'

    MEDIATYPE = 1

    @web.authenticated
    def get(self):
        mediatype = 1
        mid = self.get_argument('movie_id', None)
        eid = self.get_argument('episode_id', None)
        time = self._clean_time(self.get_argument('time', None))

        if mid:
            movie = self._get_movie(mid)
        elif eid:
            movie = self._get_episode(eid)
            self.MEDIATYPE = 2

        self._track_player(movie)

        self.render(self.tpl, **{
            'nav_active': 'movies',
            'movie': movie,
            'time': time,
            'uuid_file': self._get_uuid_file_create_session(movie),
            })

    def _track_player(self, movie):
        track = self.db.MediaTracker()
        track.ipaddr = self._get_remote_addr()
        track.userid = self.current_user._id
        track.user = self.current_user
        track.media.title = unicode(movie.title)
        track.media.collection = unicode(movie.__collection__)
        track.media.id = movie._id
        track.save()

    def _get_uuid_file_create_session(self, movie):
        uuid_file = self._create_movie_link(movie)
        self._user_movie_session(movie, uuid_file)
        return uuid_file

    def _user_movie_session(self, movie, uuid_file):
        session = self.current_user.get('session', None)
        if not session:
            # wonky
            # assign default user session from Model
            user = self.db.User()
            self.current_user['session'] = user.session

        session_uuid = session.get('uuid', None)
        if session_uuid:
            # Remove existing link
            self._delete_movie_link(session_uuid)

        self.current_user.session.movie = unicode(movie._id)
        self.current_user.session.uuid = uuid_file
        self.current_user.session.date = datetime.now()
        self.current_user.save()

    def _delete_movie_link(self, uuid_file):
        link_path = os.path.join(
            settings.static_path,
            'media/movies',
            uuid_file,
            )
        if os.path.exists(link_path):
            os.remove(link_path)

    def _create_movie_link(self, movie_obj, media_type=1):
        media_path = settings.movie_media_path
        if self.MEDIATYPE == 2:
            media_path = settings.series_media_path

        movie_uuid = unicode(uuid4())
        uuid_file = "%s.m4v" % (movie_uuid)

        real_path = os.path.join(
            media_path,
            movie_obj.filename
            )

        new_path = os.path.join(
            settings.static_path,
            'media/movies',
            uuid_file,
            )

        if not os.path.exists(real_path):
            raise NameError('Movie does not exist.')

        os.link(real_path, new_path)
        return uuid_file

    def _clean_time(self, time):
        if not time:
            return None
        try:
            return float(time)
        except:
            return None

