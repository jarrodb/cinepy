import datetime
import hashlib
import os
import re
from mongokit import Document, ObjectId
from forms.series import SERIES_TYPE

class Media(Document):
    __database__ = 'cinepy'
    __collection__ = 'media'

    structure = {
        'title': unicode,
        'sort_title': unicode,              # The Movie (sort by: Movie)
        'mediatype': int,                   # movie, series, audio

        'description': unicode,             # general data
        'genres': [unicode],                # multiple genre support
        'date': datetime.datetime,  # release date
        'date_create': datetime.datetime,   # date created in cinepy
        'poster': unicode,          #

        'enabled': bool,
    }

    validators = {
        #'title': lambda x: re.match(r'^[\w\-\.\s\,\d\_]+$', x),
    }

    use_dot_notation = True

    required_fields = [
        'title',
        'mediatype',
        ]

    default_values = {
        'mediatype': 1,
        'enabled': True,
        'date_create': datetime.datetime.utcnow,
        }

    indexes = [
        {'fields': ['title'], 'unique': True},
    ]

    mediatype_table = {
        1: 'movie',
        2: 'series',
        3: 'audio',
        }

    def get_url(self):
        if self.is_movie():
            return '/movie/%s' % (self._id)
        elif self.is_series():
            return '/series/%s' % (self._id)

    def get_poster_url(self):
        if self.poster:
            return u'/static/media/posters/%s' % (self.poster)
        return u'/static/images/movie-poster-template.jpg'

    def mediatype_display(self):
        return self.mediatype_table(self.mediatype)

    def is_movie(self):
        return self.mediatype == 1

    def is_series(self):
        return self.mediatype == 2

    def get_date_formatted(self):
        if not self.date:
            return u''
        return self.date.strftime('%b %d %Y')

    def get_length_formatted(self):
        if not self.date:
            return u''

        try:
            h, m, s = self.length.split(':')
            if h[0] == '0':
                h = h[1:]
            return u'%shr %sm' % (h, m)
        except:
            return u''


class Episode(Document):
    """ Episodes are apart of Seasons
        - order will be determined by list index
    """
    __database__ = 'cinepy'
    __collection__ = 'episodes'

    use_dot_notation = True

    structure = {
        'title': unicode,
        'desription': unicode,
        'filename': unicode,        # name of media (i.e. movie.mp4)
        'series': ObjectId,         # Use this to determine whether assigned
    }


class Season(Document):
    __database__ = 'cinepy'
    __collection__ = 'season'

    use_dot_notation = True
    use_autorefs = True

    structure = {
        'description': unicode,
        'episodes': [Episode],
        'date': datetime.datetime,  # release date
    }


class Series(Media):
    __database__ = 'cinepy'
    __collection__ = 'media'

    structure = {
        'directors': [unicode],
        'actors': [unicode],
        'rating': unicode,          # TV-G, etc
        'seriestype': int,          # Series w/ Seasons, Mini-series
        'network': unicode,         # CBS, NBC, HBO, etc
        'seasons': [Season],
    }

    validators = {
        #'title': lambda x: re.match(r'^[\w\-\.\s\,\d\_]+$', x),
    }

    use_dot_notation = True
    use_autorefs = True

    required_fields = [
        'seriestype',
        ]

    default_values = {
        'seriestype': 1,
        'mediatype': 2,
        }

    seriestype_table = {
        1: 'Series',
        2: 'Mini-Series',
        }

    def get_url(self):
        # /show/<show name>/season/<episode_id>.m4v
        # dont follow the above (lol)
        return '/series/%s' % (self._id)

    def get_series_display(self):
        for i in SERIES_TYPE:
            if i[0] == self.seriestype:
                return i[1]
        return u'Unknown'

    def is_miniseries(self):
        return self.seriestype == 2

    def is_tvseries(self):
        return self.seriestype == 1


class Movie(Media):
    __database__ = 'cinepy'
    __collection__ = 'media'

    use_schemaless = True

    structure = {
        'filename': unicode,        # name of media (i.e. movie.mp4)
        'length': unicode,          # text representation

        'directors': [unicode],
        'actors': [unicode],
        'rating': unicode,
        'trailer_id': unicode,
    }

    default_values = {
        'poster': u'default.jpg',
        }

    required_fields = [
        'filename',
        ]

    def get_url(self):
        # check mediatype later
        return '/movie/%s' % (self._id)



