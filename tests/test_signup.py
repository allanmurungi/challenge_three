import os
import unittest
 
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
        response=self.signup("","","");
        self.assertEqual(response.status_code, 400)
        assert b'you have not entered any details' in response.data
        
    def test_signup_missing_password1(self):
        response=self.signup("p@gmail.com","qwertyuiop","");
        self.assertEqual(response.status_code, 400)
        assert b'second password missing' in response.data

    def test_sgnup_missing_password2(self):
        response=self.signup("p@gmail.com","","qwertyuiop");
        self.assertEqual(response.status_code, 400)
        assert b'password missing' in response.data
        
    def test_signup_missing_email(self):
        response=self.signup("","qwertyuiop","qwertyuiop");
        self.assertEqual(response.status_code, 400)
        assert b'email address not given' in response.data
        
   
     

    def signup(self,email,password1,password2):
        return self.app.post('/signup',data=dict(email=email,password1=password1,password2=password2),follow_redirects=True);

    #### tear down  ####    
    # executed after each test
    def tearDown(self):
        pass

    
        

 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        
 
 
if __name__ == "__main__":
    unittest.main()

