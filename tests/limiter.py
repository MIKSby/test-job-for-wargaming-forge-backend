import unittest
from requests import get
from app import limit_per_minute as current_limit
from random import choice


class TestLimiter(unittest.TestCase):

    def test_limiter(self):
        # Server reboot needed before
        url = 'http://127.0.0.1:8080/'
        for i in range(current_limit):
            correct_req = get(url=url + choice(('ping', 'cats')))
            self.assertEqual(correct_req.status_code, 200)
        incorrect_req = get(url=url + choice(('ping', 'cats')))
        self.assertEqual(incorrect_req.status_code, 429)


if __name__ == '__main__':
    unittest.main()
