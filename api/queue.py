from tornado import escape
from tornado import web
from libs.torn.decorators import user_passes
from libs.torn.base import BaseHandler, MovieBaseHandler

#http://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value

class QueueHandler(MovieBaseHandler):
    @web.authenticated
    def post(self):
        try:
            movie_id = self.get_argument('movie_id')
            movie = self._get_media(movie_id)

            queue = self._get_user_queue()
            if movie not in queue.media: queue.media.append(movie)
            queue.save()

        except Exception, e:
            self.write({'error': e.message})
        else:
            self.write({
                'success': True,
                'position': queue.media.index(movie)+1,
                })

    @web.authenticated
    def delete(self):
        try:
            movie = self._get_media(self.get_argument('movie_id'))
            queue = self._get_user_queue()
            if movie in queue.media: queue.media.pop(movie)
            queue.save()

        except Exception, e:
            self.write({'error': e.message})
        else:
            self.write({
                'success': True,
                'position': queue.media.index(movie)+1,
                })

    def _get_user_queue(self):
        queue = self.db.Queue.find_one({'user._id':self.current_user._id})
        if not queue:
            queue = self.db.Queue()
            queue.user = self.current_user

        return queue

