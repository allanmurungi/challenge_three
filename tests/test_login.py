import os
import unittest
from app import app

 
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
        """"""
        response=self.login("","qwertyuiop");
        self.assertEqual(response.status_code, 400)
        assert b'no username or email entered' in response.data
        
        
    def test_login_missing_password(self):
        response=self.login("p@gmail.com","");
        self.assertEqual(response.status_code, 400)
        assert b'no password given' in response.data    
        
    

    
    
    
        
    def test_login_empty_params(self):
        response=self.login("","");
        self.assertEqual(response.status_code, 400)
        assert b'you have not entered email and password' in response.data
           

    

        
    def login(self,email,password1):
        return self.app.post('/login',data=dict(email=email,password1=password1),follow_redirects=True);
            


    
    # setup #
    # executed after each test
    def tearDown(self):
        pass

    
        

 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        
 
 
if __name__ == "__main__":
    unittest.main()

