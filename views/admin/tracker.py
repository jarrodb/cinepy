from tornado import escape
from tornado import web
from mongokit import ObjectId
from libs.torn.base import ViewHandler
from libs.torn.forms import TornadoMultiDict
from libs.models.pager import Paginator
from libs.torn.decorators import user_passes
import re


class TrackerHandler(ViewHandler):
    tpl = 'admin/tracker/tracker.html'

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        # Paginate
        mediatracker = self._get_tracker_type(1)
        logintracker = self._get_tracker_type(2)

        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'trackusers',
            'mediatracker': mediatracker,
            'logintracker': logintracker,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    def _get_tracker_type(self, ttype, limit=30):
        return self.conn.LoginTracker.find({
            'ttype':ttype
            }).sort('date', -1).limit(limit)
