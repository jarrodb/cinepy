import wtforms

def image_content_types(self, field):
    if field.data:
        raise wtforms.ValidationError('example')


class LoginForm(wtforms.Form):
    username = wtforms.TextField(
        u'Username',
        [wtforms.validators.required(), wtforms.validators.length(max=15)]
        )
    password = wtforms.TextField(
        u'Password',
        [wtforms.validators.required(), wtforms.validators.length(max=40)]
        )

