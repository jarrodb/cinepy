import wtforms
from libs.forms.fields import UnicodeField

USER_TYPES = (
    (1,'Admin'),
    (2,'Moderator'),
    (3,'Viewer'),
    (4,'Limited Viewer'),
    )


class PasswordForm(wtforms.Form):
    # Must be different name than the Document model
    passwd = UnicodeField(
        u'Password',
        [
            wtforms.validators.Optional(),
            wtforms.validators.length(max=50),
            wtforms.validators.EqualTo(
                'confirm',
                message='Passwords must match'
                )
            ],
        widget = wtforms.widgets.PasswordInput()
        )

    confirm = wtforms.PasswordField(u'Password Verify')


class UserForm(wtforms.Form):
    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)

        if kwargs.get('update', None):
            self['passwd'].validators.append(wtforms.validators.Optional())
            self['passwd'].flags.required = False
        else:
            self['passwd'].validators.append(wtforms.validators.Required())

    name = UnicodeField(
        u'Name',
        [wtforms.validators.Required(), wtforms.validators.length(max=75)],
        description='Enter full name of user',
        )

    email = UnicodeField(
        u'E-mail',
        [wtforms.validators.Required(), wtforms.validators.length(max=50)],
        description='This will be the user\'s login',
        )

    # Must be different name than the Document model
    passwd = UnicodeField(
        u'Password',
        [
            wtforms.validators.length(max=50),
            wtforms.validators.EqualTo(
                'confirm',
                message='Passwords must match'
                )
            ],
        widget = wtforms.widgets.PasswordInput()
        )

    confirm = wtforms.PasswordField(u'Password Verify')

    usertype = wtforms.SelectField(
        u'User Type',
        choices=USER_TYPES,
        coerce=int,
        )

