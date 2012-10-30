from libs.testing import ApiTest
from hashlib import md5
from nose.tools import set_trace

class UserTest(ApiTest):

    USER_DATA = {
        'company': u'billybob, inc',
        'contact': u'billy bob',
        'email': u'billy@bob.com',
        'password': unicode(md5('billy').hexdigest()),
        'usertype': 5,
        'billing': {
            'rate': 0.00,
            'increment': 0,
            }
        }

    def test_create_and_delete_user(self):
        # Create
        jd = self._d(
            '/user',
            method='POST',
            body=self.USER_DATA,
            body_type='json'
            )
        self.assertEquals(jd.get('response_code'), 200)
        self.assertIn('_id', jd)

        # Delete
        jd = self._d(
            '/user/%s' % (jd.get('_id')['$oid']),
            method='DELETE',
            )
        self.assertEquals(jd.get('response_code'), 200)
        self.assertEquals(jd.get('success'), True)

    def test_create_user_bad_schema(self):
        bad_data = self.USER_DATA
        bad_data['BAD_KEY'] = u'FAIL'
        jd = self._d(
            '/user',
            method='POST',
            body=bad_data,
            body_type='json'
            )
        self.assertEquals(jd.get('response_code'), 400)
        self.assertEquals(jd.get('success'), False)

