import Cookie
import base64
import binascii
import calendar
import datetime
import email.utils
import functools
import gzip
import hashlib
import hmac
import httplib
import itertools
import logging
import mimetypes
import os.path
import re
import stat
import sys
import time
import tornado
import traceback
import types
import urllib
import urlparse
import uuid

from tornado.web import RequestHandler
from tornado import escape
from tornado import locale
from tornado import stack_context
from tornado import template
from tornado.escape import utf8, _unicode
from tornado.options import options
from tornado.util import b, bytes_type, import_object


def asynchronous(method):
    """Wrap request handler methods with this if they are asynchronous.

    If this decorator is given, the response is not finished when the
    method returns. It is up to the request handler to call self.finish()
    to finish the HTTP request. Without this decorator, the request is
    automatically finished when the get() or post() method returns. ::

       class MyRequestHandler(web.RequestHandler):
           @web.asynchronous
           def get(self):
              http = httpclient.AsyncHTTPClient()
              http.fetch("http://friendfeed.com/", self._on_download)

           def _on_download(self, response):
              self.write("Downloaded!")
              self.finish()

    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.application._wsgi:
            raise Exception("@asynchronous is not supported for WSGI apps")
        self._auto_finish = False
        with stack_context.ExceptionStackContext(
            self._stack_context_handle_exception):
            return method(self, *args, **kwargs)
    return wrapper


class StaticFileHandler(RequestHandler):
    """A simple handler that can serve static content from a directory.

    To map a path to this handler for a static data directory /var/www,
    you would add a line to your application like::

        application = web.Application([
            (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
        ])

    The local root directory of the content should be passed as the "path"
    argument to the handler.

    To support aggressive browser caching, if the argument "v" is given
    with the path, we set an infinite HTTP expiration header. So, if you
    want browsers to cache a file indefinitely, send them to, e.g.,
    /static/images/myimage.png?v=xxx. Override ``get_cache_time`` method for
    more fine-grained cache control.
    """
    CACHE_MAX_AGE = 86400*365*10 #10 years

    def initialize(self, path, default_filename=None):
        self.root = os.path.abspath(path) + os.path.sep
        self.default_filename = default_filename

    def head(self, path):
        self.get(path, include_body=False)

    @asynchronous
    def get(self, path, include_body=True):
        #logging.info('static request %s, %s' % (self.request.uri,  self.request.headers))
        if os.path.sep != "/":
            path = path.replace("/", os.path.sep)
        abspath = os.path.abspath(os.path.join(self.root, path))
        # os.path.abspath strips a trailing /
        # it needs to be temporarily added back for requests to root/
        if not (abspath + os.path.sep).startswith(self.root):
            raise HTTPError(403, "%s is not in root static directory", path)
        if os.path.isdir(abspath) and self.default_filename is not None:
            # need to look at the request.path here for when path is empty
            # but there is some prefix to the path that was already
            # trimmed by the routing
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/")
                return
            abspath = os.path.join(abspath, self.default_filename)
        if not os.path.exists(abspath):
            raise HTTPError(404)
        if not os.path.isfile(abspath):
            raise HTTPError(403, "%s is not a file", path)
        self.set_extra_headers(path)

        stat_result = os.stat(abspath)
        
        mime_type, encoding = mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        self.set_header('Accept-Ranges','bytes')

        self.file = open(abspath, "rb")
        self._transforms = []

        if 'Range' not in self.request.headers:
            modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])
            self.set_header("Last-Modified", modified)

            cache_time = self.get_cache_time(path, modified, mime_type)
            if cache_time > 0:
                self.set_header("Expires", datetime.datetime.utcnow() + \
                                           datetime.timedelta(seconds=cache_time))
                self.set_header("Cache-Control", "max-age=" + str(cache_time))
            else:
                self.set_header("Cache-Control", "public")

            # Check the If-Modified-Since, and don't send the result if the
            # content has not been modified
            ims_value = self.request.headers.get("If-Modified-Since")
            if ims_value is not None:
                date_tuple = email.utils.parsedate(ims_value)
                if_since = datetime.datetime.fromtimestamp(time.mktime(date_tuple))
                if if_since >= modified:
                    self.set_status(304)
                    self.finish()
                    return

            self.bytes_start = 0
            self.bytes_end = stat_result.st_size - 1
            if not include_body:
                self.file.close()
                self.finish()
                return
        else:
            logging.info('got range string %s' % self.request.headers['Range'])
            self.set_status(206)
            rangestr = self.request.headers['Range'].split('=')[1]
            start, end = rangestr.split('-')
            logging.info('seeking to start %s' % start)
            self.bytes_start = int(start)
            self.file.seek(self.bytes_start)
            if not end:
                self.bytes_end = stat_result.st_size - 1
            else:
                self.bytes_end = int(end)

            clenheader = 'bytes %s-%s/%s' % (self.bytes_start, self.bytes_end, stat_result.st_size)
            self.set_header('Content-Range', clenheader)
            self.set_header('Content-Length', self.bytes_end-self.bytes_start+1)
            logging.info('set content range header %s' % clenheader)

        if 'If-Range' in self.request.headers:
            logging.debug('staticfilehandler had if-range header %s' % self.request.headers['If-Range'])


        self.bytes_remaining = self.bytes_end - self.bytes_start + 1
        self.set_header('Content-Length', str(self.bytes_remaining))
        self.bufsize = 4096 * 16
        #logging.info('writing to frontend: %s' % self._generate_headers())
        self.flush() # flush out the headers
        self.stream_one()

    def stream_one(self):
        if self.request.connection.stream.closed():
            self.file.close()
            return

        if self.bytes_remaining == 0:
            self.file.close()
            self.finish()
        else:
            data = self.file.read(min(self.bytes_remaining, self.bufsize))
            self.bytes_remaining -= len(data)
            #logging.info('read from disk %s, remaining %s' % (len(data), self.bytes_remaining))
            self.request.connection.stream.write( data, self.stream_one )

    def set_extra_headers(self, path):
        """For subclass to add extra headers to the response"""
        pass

    def get_cache_time(self, path, modified, mime_type):
        """Override to customize cache control behavior.

        Return a positive number of seconds to trigger aggressive caching or 0
        to mark resource as cacheable, only.

        By default returns cache expiry of 10 years for resources requested
        with "v" argument.
        """
        return self.CACHE_MAX_AGE if "v" in self.request.arguments else 0


