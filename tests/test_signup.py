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

