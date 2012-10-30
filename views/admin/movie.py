from tornado import escape
from tornado import web
from mongokit import ObjectId
from libs.torn.base import ViewHandler, MovieBaseHandler
from libs.torn.forms import TornadoMultiDict
from libs.torn.decorators import user_passes
from libs.models.pager import Paginator
from libs.movie import MovieStager, MovieFile
from forms.movie import MoviesImportForm
from settings import settings
import os
import re


class AddHandler(MovieBaseHandler):
    tpl = 'admin/movie/add.html'

    RESULTS_PER_PAGE = 15

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        pager = None
        page = int(self.get_argument('page', 1))

        movies = MovieStager(settings.movie_staging_path)
        movies.limit(self.RESULTS_PER_PAGE)
        if page > 1:
            movies.skip(self.RESULTS_PER_PAGE * (page-1))

        pager = Paginator(movies, page, self.RESULTS_PER_PAGE)

        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'addmovie',
            'moviesform': MoviesImportForm(obj=movies),
            'page': pager,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def post(self):
        moviesform = MoviesImportForm(TornadoMultiDict(self.request.arguments))
        count = 0
        try:
            movie_add_list = []
            # Loop through the individual forms and
            # validate the ones that are marked for
            # import.
            for mform in moviesform.movies:
                if mform.selected.data:
                    form = mform.form
                    self._validate_or_exception(form)
                    movie_add_list.append(form)
                    count += 1

            for mform in movie_add_list:
                self._add_movie_from_form(mform)

        except Exception, e:
            class Page: pass
            page = Page()
            page.is_paginated = False

            self.render(self.tpl, **{
                'error': e,
                'page': page,
                'nav_active': 'admin',
                'menu_active': 'addmovie',
                'moviesform': moviesform,
                })
        else:
            if count:
                self.set_secure_cookie('updated', 'Movies have been imported.')
            self.redirect(self.reverse_url('admin-movie-add'))

    def _add_movie_from_form(self, form):
        try:
            movie = self.db.Movie()

            # Create a MovieFile object for moving
            mfile = MovieFile(form.filename.data)

            # Populate empty movie object with formdata
            self._update_doc_from_form(movie, form)

            # Set the sort title if the user does not populate
            if not movie.sort_title:
                movie.sort_title = self._get_sort_title(movie.title)

            # Move the file to the production movie path
            filename = mfile.move_file_to(settings.movie_media_path)

            # Assign new filename and save the movie to the database
            movie.filename = filename
            movie.save()

            # Download the poster AFTER the import is successful
            # so we dont mess that up if the download fails
            poster_fn = self._poster_file_from_media_file(movie.filename)
            poster_url = form.poster_url.data
            if poster_url:
                self._download_poster_image(poster_url, poster_fn)
                movie.poster = poster_fn
            movie.save() # dual writes, yay!

        except Exception, e:
            # If something failed, delete the DB entry.
            if movie.has_key('_id'):
                movie.delete()

            # Move the file back if it was moved
            new_filepath = os.path.join(settings.movie_media_path, filename)
            os.rename(new_filepath, mfile.filename)

            # Pass the exception back up the chain
            raise


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


