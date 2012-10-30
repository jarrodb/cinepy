from datetime import datetime, date
from glob import glob
import os
import re

from tornado import httpclient, escape

class MediaStager(object):
    EXT_TYPES = ['m4v', 'mp4']

    def __init__(self, filepath, title=u''):
        self._filepath = filepath
        self._media = []
        self._limit = 0 # limit of items from skip index
        self._skip = 0 # skip to index
        self._load_media_from_filepath()
        self._title = title

    def __repr__(self):
        return '<MediaCursor: %d Movies>' % (self.count())

    def __getitem__(self, index):
        return self._media[index]

    def __iter__(self):
        # return movies with skip/limit considerations
        if not self._limit:
            return iter(self._media[self._skip:])
        return iter(self._media[self._skip:(self._skip+self._limit)])

    @property
    def media(self):
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
        return len(self._media)

    def _load_media_from_filepath(self):
        media_re = re.compile('^.*\.(m4v|mp4)$')

        _media_files = []
        for root, dirnames, filenames in os.walk(self._filepath):
            for mf in filenames:
                if media_re.match(mf):
                    _media_files.append("%s/%s" % (root,mf))

        for f in _media_files:
            _media = MediaFile(f)
            self._media.append(_media)


class MediaFile(object):

    def __init__(self, filename):
        self._filename = unicode(filename)

        self._dir = unicode(os.path.dirname(filename))
        self._file = unicode(os.path.basename(filename))

    def __repr__(self):
        return u'<Media: %s>' % (self.title)

    @property
    def file(self):
        return self._file

    @property
    def filename(self):
        return self._filename

    @property
    def title(self):
        # return title from filename if tag is empty
        f = os.path.basename(self._filename)
        _title = os.path.splitext(f)[0]

        # substitutions for readability
        _title = _title.replace('_', ' ')

        return _title

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

