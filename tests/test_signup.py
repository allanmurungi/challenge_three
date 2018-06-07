import os
import unittest
from flask import json
 
from app import app
 
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    
    #### setup  ####
   
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        
        self.assertEqual(app.debug, False)
    def test_signup_empty_params(self):
        """ a test function/unit for a missing signup details """

        response=self.signup("","")
        data=json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        assert b'you have not entered any details' in data['message']
        
    def test_signup_missing_password1(self):
        """ a test function/unit for a missing password  """

        response=self.signup("p@gmail.com","")
        data=json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('second password missing' , data['message'])

        
    def test_signup_missing_email(self):
        """ a test function/unit for a missing email address """
        response=self.signup("","qwertyuiop")
        data=json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('email address not given' , data['message'])


    def test_signup_invalid_email(self):
        """ a test function/unit for an invalid email address """

        response=self.signup("Xddfvfv","qwertyuiop")
        data=json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEquals('The email address provided is invalid' , data['message']) 
    
    def test_signup_short_password(self):
        """ a test function/unit for an invalid email address """

        response=self.signup("a@gmail.com","qwer")
        data=json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The password is too short', data[1]) 
     
    def signup(self,email,password):
        return self.app.post('/signup',data=dict(email=email,password1=password),follow_redirects=True);

    #### tear down  ####    
    # executed after each test
    def tearDown(self):
        pass

    
        

 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        
 
 
if __name__ == "__main__":
    unittest.main()

