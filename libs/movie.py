from datetime import datetime, date
from glob import glob
import os
import re

from tornado import httpclient, escape

class MovieStager(object):
    EXT_TYPES = ['m4v', 'mp4']

    def __init__(self, filepath):
        self._filepath = filepath
        self._movies = []
        self._limit = 0 # limit of items from skip index
        self._skip = 0 # skip to index
        self._load_movies_from_filepath()

    def __repr__(self):
        return '<MovieCursor: %d Movies>' % (self.count())

    def __getitem__(self, index):
        return self._movies[index]

    def __iter__(self):
        # return movies with skip/limit considerations
        if not self._limit:
            return iter(self._movies[self._skip:])
        return iter(self._movies[self._skip:(self._skip+self._limit)])

    @property
    def movies(self):
        # we are an iterable-
        # this will take advantage of skip/limits
        # instead of just returning self._movies
        return self

    def skip(self, i):
        if i > self.count:
            raise IndexError
        self._skip = i

    def limit(self, l):
        self._limit = l

    def count(self):
        return len(self._movies)

    def _load_movies_from_filepath(self):
        _movie_files = []
        for ext in self.EXT_TYPES:
            glob_arg = os.path.join(self._filepath, '*.%s' % ext)
            _movie_files.extend(glob(glob_arg))

        for f in _movie_files:
            _movie = MovieFile(f)
            self._movies.append(_movie)


class MovieFile(object):

    META_ITEMS = {
        'title': {'type': unicode, 'tag': '\xa9nam'},
#        'description': {'type': unicode, 'tag': 'ldes'},
        'date': {'type': date, 'tag': '\xa9day'},
        'genres': {'type': list, 'tag': '\xa9gen'},
        'actors': {'type': list, 'tag': '\xa9ART'},
    }

    def __init__(self, filename):
        from mutagen.mp4 import MP4
        self._filename = unicode(filename)
        self._data = MP4(filename)

        self._dir = unicode(os.path.dirname(filename))
        self._file = unicode(os.path.basename(filename))
        self._title = unicode(os.path.splitext(self._file)[0])

    def __repr__(self):
        return u'<Movie: %s>' % (self.title)

    @property
    def file(self):
        return self._file

    @property
    def filename(self):
        return self._filename

    @property
    def title(self):
        _title = self.__getattr__('title')
        if _title:
            return _title

        # return title from filename if tag is empty
        f = os.path.basename(self._filename)
        _title = os.path.splitext(f)[0]

        # substitutions for readability
        _title = _title.replace('_', ' ')

        return _title

    @property
    def description(self):
        return u''

    def __getattr__(self, item):
        item_data = self.META_ITEMS.get(item, None)
        if not item_data:
            raise NameError('Movie tag does not exist')

        value = self._data.get(item_data['tag'], None)

        if item_data.get('type') is unicode:
            return unicode(value[0]) if value else u''

        if item_data.get('type') is list:
            if value:
                return [unicode(v.strip()) for v in value[0].split(',') if v]
            return []

        if item_data.get('type') is date:
            if value:
                value = datetime.strptime(value[0], '%Y-%m-%dT%H:%M:%SZ')
                return date(value.year, value.month, value.day)
            return None

        # data type not supported
        return None

    def populate_obj(self, obj):
        # Populate obj with Movie meta data
        for item in self.META_ITEMS:
            value = getattr(self, item)
            if value:
                setattr(obj, item, value)

    def move_file_to(self, new_dir):
        if not os.path.exists(new_dir):
            raise ValueError('Directory does not exist.')

        new_filename = self._get_new_filename(new_dir)

        os.rename(self.filename, new_filename)
        self._filename = new_filename
        self._file = os.path.basename(new_filename)

        return self._file

    def _get_new_filename(self, new_dir):
        # reformat the file name to remove unwanted characters
        new_filename = self._conform_file(self._file)
        new_filepath = os.path.join(new_dir, new_filename)

        i=2
        while os.path.exists(new_filepath):
            fn, xt = os.path.splitext(new_filename)
            if i > 2:
                # more than one iteration, dont keep appending _i
                old_iter = '_%d' % (i-1)
                new_iter = '_%d' % (i)
                fn = re.sub(old_iter, new_iter, fn)
            else:
                fn = '%s_%d' % (fn, i)
            new_filename = "%s%s" % (fn, xt)
            new_filepath = os.path.join(new_dir, new_filename)
            i=i+1

        return new_filepath

    def _conform_file(self, f):
        return re.sub(r'[^\.\d\w]+', '_', f)

#http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=5z4xzs7xpfmvgxe4tegvn2ke\&q=Hitch\&page_limit=1

class MovieIMDb(object):
    API_URL = 'http://www.omdbapi.com/'

    META_ITEMS = [
        'title', 'description', 'actors', 'rating', 'poster_url',
        'directors', 'date', 'genres', 'length',
        ]

    def __init__(self, title):
        self._title = title
        self._results = self._search_title()

    def __getattr__(self, name):
        if name not in self.META_ITEMS:
            raise AttributeError('Item does not exist.')

        return self._results.get(name, u'')

    @property
    def metadata(self):
        return self._results

    def _movie_data_from_response(self, resp):
        movie_data = {
            'title': resp.get('Title', u''),
            'description': resp.get('Plot', u''),
            'actors': resp.get('Actors', u''),
            'directors': resp.get('Director', u''),
            'rating': resp.get('Rated', u'').lower(),
            'genres': resp.get('Genre', u''),
            'poster_url': resp.get('Poster', u''),
            'date': self._conform_date(resp.get('Released', u'')),
            'length': self._conform_len(resp.get('Runtime', u'')),
            }

        # Clear out bad data
        for k in movie_data.keys():
            if movie_data[k].lower() == 'n/a':
                movie_data[k] = u''

        return movie_data

    def _conform_date(self, movie_date):
        try:
            _d = datetime.strptime(movie_date, '%d %b %Y')
        except:
            return u''
        return _d.strftime('%Y-%m-%d')

    def _conform_len(self, movie_length):
        try:
            h, m = re.search(r'^(\d)\s+h\s+(\d{1,2})', movie_length).groups()
            return u'%.2d:%.2d:00' % (int(h),int(m))
        except:
            return u''

    def _title_search_uri(self):
        return "%s?t=%s" % (self.API_URL, escape.url_escape(self._title))

    def _search_title(self):
        _http_client = httpclient.HTTPClient()

        title_uri = self._title_search_uri()
        resp = _http_client.fetch(title_uri)
        data = escape.json_decode(resp.body)
        return self._movie_data_from_response(data)

