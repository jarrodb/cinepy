from urllib import urlencode

class HTTPClientMixin(object):

    def get(self, url, data=None, headers=None):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data)
            if '?' in url:
                url += '&%s' % data
            else:
                url += '?%s' % data
        return self._fetch(url, 'GET', headers=headers)

    def post(self, url, data, headers=None):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data)
        return self._fetch(url, 'POST', data, headers)

    def _fetch(self, url, method, data=None, headers=None):
        self.http_client.fetch(self.get_url(url), self.stop, method=method,
                               body=data, headers=headers)
        return self.wait()

