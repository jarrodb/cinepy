from tornado import escape
from tornado import web
import re

from libs.torn.base import BaseHandler
from libs.models.pager import Paginator


class RecentHandler(BaseHandler):
    tpl = 'results/results.html'

    RESULTS_PER_PAGE = 24

    @web.authenticated
    def get(self):
        page = self.get_argument('page', 1)
        results = self._recent_media()
        page = Paginator(results, page, self.RESULTS_PER_PAGE)

        self.render(self.tpl, **{
            'page': page,
            })

    def _recent_media(self):
        return self.db.Media.find({
            'enabled': True
            }).sort('date_create', -1).limit(3)

