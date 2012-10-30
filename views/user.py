from tornado import escape
from tornado import web
from mongokit import ObjectId
from libs.torn.base import ViewHandler
from libs.torn.forms import TornadoMultiDict
from libs.models.pager import Paginator
from libs.torn.decorators import user_passes
from forms.user import UserForm, PasswordForm
import re


class BaseUserHandler(ViewHandler):
    def __init__(self, *args, **kwargs):
        super(BaseUserHandler,self).__init__(*args, **kwargs)

    def _get_user(self, uid):
        oid = ObjectId(uid)
        return self.conn.User.one({'_id': oid})

    def _admin_or_current_user(self, user_obj):
        if self.current_user.is_admin or user_obj == self.current_user:
            return True
        raise web.HTTPError(403, 'Stick to your own profile, buddy.')


class UserHandler(BaseUserHandler):
    tpl = 'user/user.html'

    @web.authenticated
    def get(self, uid=None):
        user = self.current_user if not uid else self._get_user(uid)
        self._admin_or_current_user(user)

        self.render(self.tpl, **{
            'user': user,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })


class QueueHandler(BaseUserHandler):
    tpl = 'user/queue.html'

    @web.authenticated
    def get(self, uid=None):
        user = self.current_user if not uid else self._get_user(uid)
        self._admin_or_current_user(user)

        queue = self.db.Queue.find_one({'user._id':user._id})

        self.render(self.tpl, **{
            'user': user,
            'queue': queue,
            })


class EditHandler(BaseUserHandler):
    tpl = 'user/edit.html'

    @web.authenticated
    def get(self, uid):
        user = self._get_user(uid)
        self._admin_or_current_user(user)

        form = PasswordForm()
        if self.current_user.is_admin:
            form = UserForm(obj=user, update=True)

        self.render(self.tpl, **{
            'user': user,
            'userform': form,
            })

    @web.authenticated
    def post(self, uid):
        user = self._get_user(uid)
        self._admin_or_current_user(user)

        if self.get_argument('delete', None):
            self._user_delete(user)
        else:
            self._user_edit(user)

    def _user_edit(self, user):
        try:
            post_args = TornadoMultiDict(self.request.arguments)
            if self.current_user.is_admin:
                # Admin can edit the full UserForm
                form = UserForm(post_args, update=True)
            else:
                # Users can only change their passwords
                form = PasswordForm(post_args, user)

            # Validate the form
            self._validate_or_exception(form)

            form.populate_obj(user)
            if form.passwd.data:
                user.set_password(form.passwd.data)
            user.save()

        except Exception, e:
            self.render(self.tpl, **{
                'error': e,
                'user': user,
                'userform': form,
                })
        else:
            self.set_secure_cookie('updated', 'User updated.')
            self.redirect(self.reverse_url('user', user._id))

    @user_passes(lambda user: user.is_admin)
    def _user_delete(self, user):
        user.delete()
        self.set_secure_cookie('updated', 'User deleted.')
        self.redirect(self.reverse_url('admin-users'))

