import unittest
from requests import get


class TestApiCats(unittest.TestCase):

    def test_ping(self):
        req = get(url=f'http://127.0.0.1:8080/ping')
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.json(), 'Cats Service. Version 0.1')


class TestApiCatsGet(unittest.TestCase):

    host_test = '127.0.0.1'
    port_test = '8080'

    def test_get_default(self):
        req = get(url=f'http://{self.host_test}:{self.port_test}/cats')
        self.assertEqual(req.status_code, 200)
        self.assertIsInstance(req.json(), list)

    def test_get_order_valid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?order=asc')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?order=desc')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_get_order_invalid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?order=bla')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad order!', r.json()['message']['order'])

    def test_get_attribute_valid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=name')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=color')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=tail_length')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=whiskers_length')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_get_attribute_invalid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=1')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad attribute!', r.json()['message']['attribute'])
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=-2')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad attribute!', r.json()['message']['attribute'])
        r = get(f'http://{self.host_test}:{self.port_test}/cats?attribute=bla')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad attribute!', r.json()['message']['attribute'])

    def test_get_offset_valid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=0')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=1')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=2')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_get_offset_invalid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=-1')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad offset!', r.json()['message']['offset'])
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=-2')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad offset!', r.json()['message']['offset'])
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=bla')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad offset!', r.json()['message']['offset'])

    def test_get_limit_valid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=0')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=1')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        r = get(f'http://{self.host_test}:{self.port_test}/cats?offset=2')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_get_limit_invalid(self):
        r = get(f'http://{self.host_test}:{self.port_test}/cats?limit=-1')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad limit!', r.json()['message']['limit'])
        r = get(f'http://{self.host_test}:{self.port_test}/cats?limit=-2')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad limit!', r.json()['message']['limit'])
        r = get(f'http://{self.host_test}:{self.port_test}/cats?limit=bla')
        self.assertEqual(r.status_code, 400)
        self.assertIn('Bad limit!', r.json()['message']['limit'])


if __name__ == '__main__':
    unittest.main()
