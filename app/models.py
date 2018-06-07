from passlib.hash import pbkdf2_sha256 as sha256
import re


class UserModel:
    

    @staticmethod
    def generate_hash(password):
        """ a  function for a hashing a provided entry or password """

        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        """ a  function for verifying a hashed entry or password """

        return sha256.verify(password, hash)

    @staticmethod
    def validate_login(email,password):
        """ a  function for validating  provided log-in details """
        if(email==""):
            return {'message':'no username/email entered'}
            
        elif(password==""):
            return {'message':'no password given'}
            
        elif(email=="" and password=="" ):
            return {'message':'you have not entered email and password'}
        elif(not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            return {'message':'The email address provided is invalid'}
        else:
            return True
    @staticmethod
    def validate_signup(email,password):
        """ a  function for validating  provided sign-up details"""

        if(email==""):
            return {'message':'no username/email entered'},400
            
        elif(password==""):
            return {'message':'no password given'},400
            
        elif(email=="" and password=="" ):
            return {'message':'you have not entered email and password'},400
        elif(not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            return {'message':'The email address provided is invalid'}
        elif(len(password)<6):
            return {'message':'The password is too short'}    
        else:
            return True
    @staticmethod
    def validate_create_request(entry):
        """ a  function for validating a request entry """
        pass
    
    @staticmethod
    def validate_req(entry):
        """ a  function for validating a request entry """
        if(entry==""):
            return {'message':'Missing entry'}
        else:
            return True    


class RevokedTokenModel:
    __tablename__ = 'revoked_tokens'
    
    
    def add(self):
        pass
        
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
       
        return True