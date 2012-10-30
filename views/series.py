from tornado import escape, web
from uuid import uuid4
from mongokit import ObjectId
from libs.torn.base import SeriesBaseHandler
from libs.torn.decorators import user_passes
from settings import settings
from datetime import datetime
import os
import re


class SeriesHandler(SeriesBaseHandler):
    tpl = 'series/series.html'

    @web.authenticated
    def get(self, mid):
        series = self._get_series(mid)

        self.render(self.tpl, **{
            'nav_active': 'movies',
            'subnav_active': 'movie',
            'media': series,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })


