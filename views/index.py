from tornado import escape

from libs.torn.base import MovieBaseHandler

class IndexHandler(MovieBaseHandler):
    CAROUSEL_COUNT = 4
    CAROUSEL_LIMIT = 20

    uauth_tpl = 'uaindex.html'
    auth_tpl = 'index.html'


    def get(self):
        _u = self.get_current_user()
        self.auth(_u) if _u else self.unauth()

    def auth(self, user):
        remote_ip = self._get_remote_addr()

        movies_by_genre = {
            'Action': self._genre_movie_list('Action'),
            'Comedy': self._genre_movie_list('Comedy'),
            'Family': self._genre_movie_list('Family'),
            }

        # recently watched
        rw_movie = self._get_recently_watched_movie()

        self.render(self.auth_tpl, **{
            'rw_movie': rw_movie,
            'movies_by_genre': movies_by_genre,
            })

    def _get_recently_watched_movie(self):
        rw_movie = None
        try:
            rw_time = self.current_user.session.time
            if not rw_time: return rw_movie

            session = self.current_user.get('session')
            rw_movie = self._get_media(session.movie)
            if rw_movie.has_key('length'):
                length = rw_movie.get('length')
                rw_movie.percent = self._movie_percent_watched(length, rw_time)
            else:
                # return None if Media doesn't have length defined
                rw_movie = None
        except:
            rw_movie = None
        # Return the populated movie object, or none
        return rw_movie

    def _genre_movie_list(self, genre):
        movie_list = self.conn.Media.find(
            {
                'mediatype': 1,
                'genres': genre,
                'enabled': True,
                }
            ).sort('date_create', -1).limit(self.CAROUSEL_LIMIT)
        return self._carousel_movie_list(
            [mov for mov in movie_list],
            self.CAROUSEL_COUNT
            )

    def _carousel_movie_list(self, movie_list, count):
        _list = []
        _tmp = []
        movie_len = len(movie_list)
        for i, movie in enumerate(movie_list, start=1):
            _tmp.append(movie)
            if (i%count) == 0 or i == movie_len:
                _list.append(list(_tmp))
                _tmp = []
        return _list

    def unauth(self):
        self.render(self.uauth_tpl, **{})


