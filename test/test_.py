import unittest
import requests
import httpretty
import ujson

from http import HTTPStatus

BASE_URL = 'http://localhost:4100/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
ADMIN = {"username":"bao1","password":"abc"}



def get_user_credential(type=None):
    return {
        'noname':{}
    }.get(type, ADMIN)

def get_url(entity=None):
    return BASE_URL + {
        'login': 'login2',
        'customer': 'customer'
    }.get(entity, 'login2')

def get_reponse_keys(entity=None):
    return {
        'customer' : ['deleted', 'description', 'f_changed', 'name', 'id', 'user_id', 'timestamp'],
        'user'     : ['deleted', 'f_changed', 'username', 'id', 'timestamp']
    }.get(entity,[])


def send_request(entity=None, method='GET', **kwargs):
    return {
        'GET'   : requests.get(get_url(entity), **kwargs),
        'POST'  : requests.post(get_url(entity), **kwargs ),
        'PUT'   : requests.put(get_url(entity), **kwargs )
    }.get(method, None)

class BaseTest:
    pass


class FirstTest(unittest.TestCase):
    def test_add(self):
        a = 10 + 5
        print(a)
        self.assertEquals(15, a)


class CustomAssert(unittest.TestCase):
      def assertRequestOK(self, response):
          self.assertEquals(response.status_code, HTTPStatus.OK)

class Login(unittest.TestCase, BaseTest):
    def test_login(self):
        # use!
        response = requests.post(get_url('login2'), data=ujson.dumps(get_user_credential()))
        self.assertEquals(response.status_code, HTTPStatus.OK )
        self.assertEquals(response.text, 'Login successfully !')


class Customer(unittest.TestCase, BaseTest, CustomAssert):
    def setUp(self):
        response = requests.post(get_url('login2'), data=ujson.dumps(get_user_credential()))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.text, 'Login successfully !')

    def test_get(self):
        response = send_request(entity='customer', method='GET')
        body = ujson.loads(response.text)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        for item in body:
            self.assertEquals(
                set(item.keys())^set(get_reponse_keys('customer')),
                set()
            )

    def test_post(self):
        response = send_request(entity='customer', method='POST')
        body = ujson.loads(response.text)
        self.assertRequestOK(response)


if __name__ == "__main__":
    unittest.main()