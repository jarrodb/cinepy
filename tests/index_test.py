from libs.testing import ApiTest

class IndexTest(ApiTest):
    def test_key_test(self):
        jd = self._d('/')
        self.assertEquals(jd.get('response_code'), self._http_success_code)

