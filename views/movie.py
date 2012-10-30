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
import urllib2
import shutil
import urlparse
import wtforms
import copy
import os
import re


class MoviesHandler(ViewHandler):
    tpl = 'movie/movies.html'

    RESULTS_PER_PAGE = 21
    SORT_KEY = 'sort_title'

    @web.authenticated
    def get(self):
        msform = MovieSearchForm(TornadoMultiDict(self.request.arguments))
        pager = None
        page = self.get_argument('page', 1)
        search = self.get_argument('search', None) # genre text

        #self._letter_query = {'mediatype': 1}
        self._letter_query = {'mediatype':{'$in': [1,2]}}
        self.startswith = self.get_argument('sw', 'a') # letter


        self.title = msform.title.data # movie title
        self.adname = msform.adname.data # actor / director
        self.genres = msform.genres.data # multiple genre text
        self.rating = msform.rating.data # rating

        if not search:
            results = self._all_movies()
        else:
            results = self._search_movies()

        movie_letters = self._movie_letters(self._letter_query)
        if self.startswith not in movie_letters and self.startswith != '0':
            # Will yield empty results, but will not error
            # Fix this
            movie_letters.append(self.startswith)
            movie_letters.sort()

        if results:
            pager = Paginator(results, page, self.RESULTS_PER_PAGE)

        self.render(self.tpl, **{
            'msform': msform,
            'nav_active': 'movies',
            'movie_letters': movie_letters,
            'swbtn': self.startswith,
            'page': pager,
            })

    def _movie_letters(self, query):
        all_letters = ['#']
        all_letters.extend([chr(c) for c in xrange(ord('a'), ord('z')+1)])

        if query:
            # yay aggregate groupz
            res = self.db.media.group(
                None,
                query,
                {'letter_index': {}},
                'function(obj, prev) {prev.letter_index[obj.sort_title[0].toLowerCase()] = 1 }',
                )
            try:
                _al = res[0]['letter_index'].keys()
                all_letters = self._sort_and_collapse_movie_letters(_al)
            except Exception, e:
                return []

        return all_letters

    def _sort_and_collapse_movie_letters(self, letters):
        _al = []
        for c in letters:
            if c.isdigit() and u'#' not in _al:
                _al.append(u'#')
            elif not c.isdigit():
                _al.append(c)
        _al.sort()
        return _al

    def _all_movies(self):
        # do not set self._query so all letters are found
        sw_query = re.compile('^%s' % self._startswith_query(), re.IGNORECASE)
        #'mediatype': 1,
        return self.db.Media.find({
            self.SORT_KEY: sw_query
            }).sort(self.SORT_KEY, 1)

    def _search_movies(self):
        # we are tracking multiple query arrays for finding
        # letters because of copy by reference.
        # i need to drop the startswith from the letters_query
        # because i need it to know all matches
        # fix this somehow?
        #query_array = [{'mediatype':1}]
        #self._letter_query = [{'mediatype':1}]
        query_array = [{'mediatype':{'$in': [1,2]}}, {'enabled':True}]
        self._letter_query = [{'mediatype':{'$in': [1,2]}}, {'enabled':True}]

        if self.title:
            title_re = re.compile(self.title, re.IGNORECASE)
            query_array.append({'title': title_re})
            self._letter_query.append({'title': title_re})

        if self.adname:
            adname_query = []
            name_re = re.compile(self.adname, re.IGNORECASE)
            adname_query.append({'actors': name_re})
            adname_query.append({'directors': name_re})

            query_array.append({'$or': adname_query})
            self._letter_query.append({'$or': adname_query})

        if self.genres:
            # multiple genre support
            genre_query = []
            for g in self.genres:
                g_txt = "^%s$" % (g)
                g_re = re.compile(g_txt, re.IGNORECASE)
                genre_query.append({'genres': g_re})
            query_array.append({'$or': genre_query})
            self._letter_query.append({'$or': genre_query})

        if self.rating:
            rating_query = []
            for r in self.rating:
                r_txt = "^%s$" % (r)
                r_re = re.compile(r_txt, re.IGNORECASE)
                rating_query.append({'rating': r_re})
            query_array.append({'$or': rating_query})
            self._letter_query.append({'$or': rating_query})

        # append startswith
        q = self._startswith_query()
        sw_query = re.compile('^%s' % q, re.IGNORECASE)
        query_array.append({self.SORT_KEY: sw_query})

        # movie letters bullcrap
        self._letter_query = {'$and': self._letter_query}

        return self.db.Media.find({'$and': query_array}).sort(self.SORT_KEY, 1)

    def _startswith_query(self):
        # if sw = 0, query for [0-9]
        if self.startswith.isdigit():
            return '[0-9]'
        return self.startswith


class MovieHandler(MovieBaseHandler):
    tpl = 'movie/movie.html'

    @web.authenticated
    def get(self, mid):
        movie = self._get_movie(mid)

        time, percent = self._get_time_percent(movie)

        self.render(self.tpl, **{
            'nav_active': 'movies',
            'subnav_active': 'movie',
            'media': movie,
            'time': time,
            'percent': percent,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    def _get_time_percent(self, movie):
        # checks to see if movie is the most recently watched movie
        time, percent = None, None
        session = self.current_user.get('session', None)
        if not session:
            return (time, percent)

        if unicode(movie._id) == session.get('movie', ''):
            if movie.get('length', None) and session.get('time', None):
                time = session.get('time')
                length = movie.get('length')
                percent = self._movie_percent_watched(length, time)
                return (time, percent)

        return (time, percent)


class MovieEditHandler(MovieBaseHandler):
    tpl = 'movie/edit.html'

    @web.authenticated
    @user_passes(lambda user: user.is_atleast('moderator'))
    def get(self, mid):
        movie = self._get_movie(mid)
        movieform = MovieForm(obj=movie)
        posterform = MoviePosterForm()

        self.render(self.tpl, **{
            'nav_active': 'movies',
            'movie': movie,
            'movieform': movieform,
            'posterform': posterform,
            })

    @web.authenticated
    @user_passes(lambda user: user.is_atleast('moderator'))
    def post(self, mid):
        movie = self._get_movie(mid)
        movieform = MovieForm(obj=movie)
        posterform = MoviePosterForm(obj=movie)
        try:
            torn_post_args = TornadoMultiDict(self.request.arguments)
            if self.get_argument('movieform', None):
                movieform = MovieForm(torn_post_args)
                self._validate_or_exception(movieform)
                self._update_doc_from_form(movie, movieform)
                self._assign_media_poster(movie, movieform.poster_url.data)

                # check if sort title needs changing
                if not movieform.sort_title.data:
                    # Only auto calculate if sort_title is blank
                    # so the moderators can override it.
                    new_title = movieform.title.data
                    movie.sort_title = self._get_sort_title(new_title)

                movie.save()

            elif self.get_argument('posterform', None):
                posterform = MoviePosterForm(torn_post_args)
                self._validate_or_exception(posterform)
                self._assign_media_poster(movie, posterform.poster.data)
                movie.save()

        except Exception, e:
            error = '%s' % (e)
            self.render(self.tpl, **{
                'error': error,
                'nav_active': 'movies',
                'movie': movie,
                'movieform': movieform,
                'posterform': posterform,
                })
        else:
            self.set_secure_cookie('updated', 'Thanks for adding movie data!')
            self.redirect(self.reverse_url('movie', mid))


