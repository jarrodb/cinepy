from tornado import escape
from tornado import web
import re

from libs.torn.base import BaseHandler
from libs.models.pager import Paginator


class SearchHandler(BaseHandler):
    tpl = 'results/results.html'

    RESULTS_PER_PAGE = 12

    @web.authenticated
    def get(self):
        page = self.get_argument('page', 1)
        query = self.get_argument('query', None)
        results = self._search_media(query) if query else []
        page = Paginator(results, page, self.RESULTS_PER_PAGE)

        self.render(self.tpl, **{
            'query': query,
            'page': page,
            })

    def _search_media(self, query):
        re_query = re.compile(query, re.IGNORECASE)
        query_array = [{'title': re_query}, {'actors': re_query}]

        return self.db.Media.find({'$or': query_array}).sort('sort_title', 1)

