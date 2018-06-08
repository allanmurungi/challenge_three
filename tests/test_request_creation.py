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

    def test_missing_entry(self):
        """a test for the endpoint for creating a request, this tests for missing entries input"""

        response = self.addrequest("water flow", "", "a@gmail.com", "null")
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual('Missing entry', data['message'])

        response = self.addrequest(
            "", "The water flow in the evening is terrible", "a@gmail.com", "null")
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Missing entry', data['message'])

        response = self.addrequest(
            "water flow", "The water flow in the evening is terrible", "", "null")
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Missing entry', data['message'])

        response = self.addrequest(
            "water flow", "The water flow in the evening is terrible", "a@gmail.com", "")
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Missing entry', data['message'])

    def addrequest(self, req_title, req_details, req_owner, req_status):
        return self.app.post('/createrequest', data=dict(req_title=req_title, req_details=req_details, req_owner=req_owner, req_status=req_status), follow_redirects=True)

    # setup #
    # executed after each test

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
