import functools
from tornado.web import HTTPError

def user_passes(pass_func):
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not (self.current_user and pass_func(self.current_user)):
                raise HTTPError(403)
            return method(self, *args, **kwargs)
        return wrapper
    return wrap


