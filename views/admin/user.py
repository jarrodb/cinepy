from tornado import escape
from tornado import web
from mongokit import ObjectId
from libs.torn.base import ViewHandler
from libs.torn.forms import TornadoMultiDict
from libs.models.pager import Paginator
from libs.torn.decorators import user_passes
from forms.user import UserForm
import re


class UsersHandler(ViewHandler):
    tpl = 'admin/user/users.html'

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        users = self.conn.User.find().sort('name', -1).limit(30)
        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'listusers',
            'users': users,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })


class AddHandler(ViewHandler):
    tpl = 'admin/user/add.html'

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'adduser',
            'userform': UserForm(),
            })

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def post(self):
        userform = UserForm(TornadoMultiDict(self.request.arguments))

        try:
            self._validate_or_exception(userform) # Validate Form
            new_user = self.db.User() # Declare a blank User model
            userform.populate_obj(new_user) # Populate User with form data
            new_user.set_password(userform.passwd.data)
            new_user.save()
        except Exception, e:
            self.render(self.tpl, **{
                'error': e,
                'nav_active': 'admin',
                'menu_active': 'adduser',
                'userform': userform,
                })
        else:
            self.set_secure_cookie('updated', 'User added.')
            self.redirect(self.reverse_url('admin-users'))

