import json
import wtforms
import urllib2
import shutil
import tornado.web
import os
import re
from datetime import datetime, date
from mongokit import ObjectId
from settings import settings
from hashlib import md5

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler,self).__init__(*args, **kwargs)
        self.conn = self.application.settings.get('connection')
        self.db = self.conn[settings.mongo_dbname]

    def get_current_user(self):
        try:
            _u = json.loads(self.get_secure_cookie('authed_user'))
            # query memcache here
            return self.db.User.find_one({'_id':ObjectId(_u['user'])})
        except:
            return None

    def set_current_user(self, user):
        self.set_secure_cookie(
            'authed_user',
            json.dumps({'user':str(user)}),
            expires_days=3,
            )

    def clear_current_user(self):
        self.set_secure_cookie('authed_user', '')

    def auth_user(self, email, passwd):
        _u = self.conn.User.find_one({
            'email': email,
            'password': md5(passwd).hexdigest()
            })
        return _u

    def get_and_clear_secure_cookie(self, key):
        val = self.get_secure_cookie(key, None)
        self.set_secure_cookie(key, '')
        return val

    def get_args_uri(self, exclude=[]):
        q = '?'
        for key in self.request.arguments:
            if not key in exclude:
                for val in self.get_arguments(key):
                    q += '%s=%s&' % (key, val)
        return q

    def get_args_form(self, exclude=[]):
        inputs = ''
        tpl = '<input type="hidden" name="%s" value="%s">'
        for key in self.request.arguments:
            if not key in exclude:
                for val in self.get_arguments(key):
                    inputs += tpl % (key, val)
        return inputs

    def render_string(self, template_name, **kwargs):
        kwdef = {
            'error': None,
            'query': None,
            'updated': None,
            'notification': None,
            'nav_active': 'home',
            'site_url': settings.site_url,
            }
        kwdef.update(kwargs)

        return super(BaseHandler, self).render_string(template_name, **kwdef)

    # private
    def _get_remote_addr(self):
        remote_ip = self.request.headers.get('X-Forwarded-For', None)
        if not remote_ip:
            remote_ip = self.request.remote_ip
        return unicode(remote_ip)



#    def get_error_html(self, status_code, **kwargs):
#        return self.oops(
#            "Something bad has happened. Perhaps refreshing will fix it?",
#            )

class ViewHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ViewHandler,self).__init__(*args, **kwargs)

    def _validate_or_exception(self, form):
        if not form.validate():
            raise wtforms.validators.ValidationError('Invalid Form')

    def _update_doc_from_form(self, doc, form, exclude=None):
        # exclude should be a list of strings that are form elements
        # that should not be assigned
        if not exclude or not isinstance(exclude, list):
            exclude = []

        # Let's assume something changed if you clicked 'Update'
        # You can refactor later ...
        # ... yea right
        change = 1

        for field in form:
            name = field.short_name # Use short_name for FieldLists
            data = field.data

            # compare or just assign it
            if isinstance(data, list):
                # strip empty items
                data = filter(None, data)
                # assume the form validated the data accordingly

            elif isinstance(data, str) or isinstance(data, unicode):
                # for good measure
                data = data.decode('utf-8')

            elif isinstance(data, date):
                # mongokit documents only support datetime, DOH!
                data = datetime(data.year, data.month, data.day)

            elif isinstance(data, bool) and not name in exclude:
                # False will not pass the below statement
                setattr(doc, name, data)

            if not name in exclude and data:
                setattr(doc, name, data)

###
class MediaBaseHandler(ViewHandler):
    def _assign_media_poster(self, media, poster_url):
        poster_fn = self._poster_file_from_media_file(media.filename)
        if poster_url:
            self._download_poster_image(poster_url, poster_fn)
            media.poster = poster_fn

    def _poster_file_from_media_file(self, filename):
        basefn = os.path.basename(filename)
        fn, fe = os.path.splitext(basefn)
        # lets just go with jpg for now
        return u'%s.jpg' % (fn)

    def _download_poster_image(self, url, filename):
        fullfile = os.path.join(
            settings.static_path,
            'media/posters',
            filename
            )
        r = urllib2.urlopen(urllib2.Request(url))
        try:
            with open(fullfile, 'wb') as f:
                shutil.copyfileobj(r,f)
        except:
            raise
        finally:
            r.close()

    def _get_new_poster_file(self, filename, mtype='tv'):
        # force poster to .jpg
        fn, xt = os.path.splitext(filename)
        fn = self._conform_file(fn)
        new_filename = "%s_%s.jpg" % (fn, mtype)
        return new_filename

    def _conform_file(self, f):
        return re.sub(r'[^\.\d\w]+', '_', f)

    def _get_media(self, mid):
        oid = ObjectId(mid)
        return self.conn.Media.one({'_id': oid})

    def _movie_percent_watched(self, length, current_time):
        duration = self._length_to_seconds(length)
        percent = int((current_time/duration) * 100)
        return percent

    def _length_to_seconds(self, length):
        # HH:MM:SS
        try:
            total = 0.0
            h, m, s = length.split(':')
            h, m, s = int(h), int(m), int(s)
            total += h*60*60
            total += m*60
            total += s
        except:
            return 0.0
        return float(total)

###
class MovieBaseHandler(MediaBaseHandler):

    def _get_movie(self, mid):
        oid = ObjectId(mid)
        return self.conn.Movie.one({'_id': oid})

    def _get_episode(self, eid):
        oid = ObjectId(eid)
        return self.conn.Episode.one({'_id': oid})

    def _get_sort_title(self, title):
        a_re = re.compile('^[A|a]\s(.*)$')
        an_re = re.compile('^[A|a]n\s(.*)$')
        the_re = re.compile('^[T|t]he\s(.*)$')

        try:
            if a_re.match(title):
                return a_re.match(title).group(1)
            elif an_re.match(title):
                return an_re.match(title).group(1)
            elif the_re.match(title):
                return the_re.match(title).group(1)

            return title
        except:
            # crap, just return the title
            return title

###
class SeriesBaseHandler(MediaBaseHandler):

    def _get_series(self, sid):
        oid = ObjectId(sid)
        return self.conn.Series.one({'_id': oid})

