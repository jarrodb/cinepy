from tornado import escape, web
from libs.torn.base import ViewHandler
from hashlib import md5
import json
import re


class LoginHandler(ViewHandler):
    login_tpl = 'uaindex.html'

    def get(self):
        self.render(self.login_tpl, **{
            'error_msg': 'Login Required',
            })

    def post(self):
        _u = self.auth_user(
            self.get_argument('username', ''),
            self.get_argument('password', '')
            )

        if not _u:
            self.render(self.login_tpl, **{
                'error_msg': 'Invalid Credentials',
                })
        else:
            self.set_current_user(str(_u.get('_id')))
            self._track_auth(_u)
            self.redirect(self.reverse_url('index'))

    def _track_auth(self, user):
        track = self.db.LoginTracker()
        track.ipaddr = self._get_remote_addr()
        track.userid = user._id
        track.user = user
        track.save()


class LogoutHandler(ViewHandler):
    def get(self):
        self.clear_current_user()
        self.redirect(self.reverse_url('index'))

