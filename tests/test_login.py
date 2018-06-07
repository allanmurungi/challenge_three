import os
import unittest
from app import app
from flask import json


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    """a test class for the login feature"""
    # setup #

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def test_login_missing_email(self):
        """a test for the login end point"""

        response = self.login("", "qwertyuiop")
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        assert b'no username or email entered' in data['message']

    def test_login_missing_password(self):
        """a test for the login end point"""

        response = self.login("p@gmail.com", "")
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        assert b'no password given' in data['message']

    def test_login_invalid_email(self):
        """ a test function/unit for an invalid email address """

        response = self.login("Xddfvfv", "qwertyuiop")

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        assert b'The email address provided is invalid' in data['message']

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password1=password), follow_redirects=True)

    # setup #
    # executed after each test

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
