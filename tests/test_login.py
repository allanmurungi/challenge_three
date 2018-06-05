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
        self.assertEqual(response.status_code, 401)
        assert b'no username/email entered' in response.data
        
        
    def test_login_missing_password(self):
        response=self.login("p@gmail.com","");
        self.assertEqual(response.status_code, 401)
        assert b'no password given' in response.data    
        
    def test_login_default_admin(self):
        response=self.login("admin@andela.com","default");
        self.assertEqual(response.status_code, 200)
        assert b'you have logged in as default admin' in response.data

    def test_succesful_login(self):
        response=self.login("p@gmail.com","qwertyuiop");
        self.assertEqual(response.status_code, 200)
        assert b'you have logged in succesfully' in response.data

            
    def test_succesful_login_fail(self):
        response=self.login("x@gmail.com","hhfhf");
        self.assertEqual(response.status_code, 401)
        assert b"Wrong credentials" in response.data
        
    def test_succesful_login_user_not_exist(self):
        response=self.login("x@gmail.com","qwertyuiop");
        self.assertEqual(response.status_code, 401)
        assert b'User doesn\'t exist' in response.data
        
    def test_login_empty_params(self):
        response=self.login("","");
        self.assertEqual(response.status_code, 400)
        assert b'you have not entered email and password' in response.data
           

    

        
    def login(self,email,password):
        return self.app.post('/login',data=dict(email=email,password=password),follow_redirects=True);
            


    
    # setup #
    # executed after each test
    def tearDown(self):
        pass

    
        

 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        
 
 
if __name__ == "__main__":
    unittest.main()

