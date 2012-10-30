from tornado import escape
from tornado import web
from libs.torn.decorators import user_passes
from libs.torn.base import BaseHandler
from libs.movie import MovieIMDb

class MetaHandler(BaseHandler):
    @web.authenticated
    @user_passes(lambda user: user.is_atleast('Moderator'))
    def get(self):
        title = self.get_argument('title', None)
        try:
            if not title:
                raise ValueError('Must specify a title')

            m = MovieIMDb(title)
            self.write(m.metadata)
        except Exception, e:
            self.write()
        finally:
            self.finish()


class TimeHandler(BaseHandler):
    @web.authenticated
    def post(self):
        movie_id = self.get_argument('movie_id')
        current_time = self.get_argument('time')

        if self.current_user.session.movie == movie_id:
            # try/except float() ?
            self.current_user.session.time = float(current_time)
            self.current_user.save()
            self.write({'success': True})
        else:
            self.write({'success': False})

