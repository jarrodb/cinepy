import re

class Paginator(object):
    def __init__(self, cursor, page=1, limit=10):
        self._cursor = cursor
        self._count = self._cursor.count() if cursor else 0
        self._limit = limit
        self._page = int(page)
        self._set_page(self._page)

    @property
    def items(self):
        return self._cursor

    @property
    def is_paginated(self):
        return self.num_pages > 1

    @property
    def start_index(self):
        if self._page == 1: return 1
        if self._limit == 1: return self._page
        return ((self._page-1) * self._limit) + 1

    @property
    def end_index(self):
        if self._limit == 1: return self._page

        if self._page == 1:
            return self._count if self._count < self._limit else self._limit

        calc_end = (self._page * self._limit)
        return calc_end if calc_end < self._count else self._count

    @property
    def current_page(self):
        return self._page

    @property
    def previous_page(self):
        return self._page - 1

    @property
    def next_page(self):
        return self._page + 1

    @property
    def has_next(self):
        return self.end_index < self._count

    @property
    def has_previous(self):
        return self.start_index - self._limit >= 0

    @property
    def page_range(self):
        return [p for p in xrange(1, self.num_pages+1)]

    @property
    def num_pages(self):
        if self._count <= 0: return 0
        if self._count <= self._limit: return 1

        pages_f = self._count / float(self._limit)
        pages_i = int(pages_f)

        return (pages_i + 1) if pages_f > pages_i else pages_i

    @property
    def count(self):
        return self._count

    def _set_page(self, page_num):
        if self._page > 1:
            self._cursor.skip(self.start_index - 1)

        if self._cursor:
            self._cursor.limit(self._limit)


