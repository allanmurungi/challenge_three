from app import app
from flask import jsonify
import json
from flask_restful import Resource, Api, reqparse
from app.models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import random


parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password1', help = 'This field cannot be blank', required = True)

parser_2 = reqparse.RequestParser()
parser_2.add_argument('email', help = 'This field cannot be blank', required = True)
parser_2.add_argument('password1', help = 'This field cannot be blank', required = True)
parser_2.add_argument('password2', help = 'This field cannot be blank', required = True)

api = Api(app)



class myrequest:
    """ A template class for the request object """
    def __init__(self,req_title,req_details,req_owner):
        """ the constructor"""
        self.title=req_title
        self.details=req_details
        self.req_id=random.randint(1,1000000)
        self.req_owner=req_owner
     
    def getId(self):
        return self.req_id

    def getreqtitle(self):
        return self.title

    def getreqdetails(self):
        return self.details

    def getreqemail(self):
        return self.req_owner

    

class myIndex(Resource):
    def get(self):
        return  'maintenance tracker endpoints!';
    def post(self):
        return  'maintenance tracker endpoints post!';


class login(Resource):
    def post(self):
        data = parser.parse_args()
        #current_user = UserModel.find_by_email(data['email']) // call model function to check for his existence
        if(data['email']=="" and data['password1']!=""):
            return 'no username or email entered',400
            
        elif(data['password1']=="" and data['email']!=""):
            return 'no password given',400
            
        elif(data['email']=="" and data['email']=="" ):
            return 'you have not entered email and password',400
            
        #if not current_user:
            #return {'message': 'User doesn\'t exist'}
        
        #if UserModel.verify_hash(data['password'], current_user.password):
           # access_token = create_access_token(identity = data['email'])
           # refresh_token = create_refresh_token(identity = data['email'])
        try:
            #new_user.save_to_db()
            #access_token = create_access_token(identity = data['email'])
            #refresh_token = create_refresh_token(identity = data['email'])
            #return {
                #'message': 'User {} was created'.format(data['email']),
                #'access_token': access_token,
                #'refresh_token': refresh_token
               # },201
            return  'you have logged in succesfully',200    
        except:
            return 'Wrong credentials', 401


class signup(Resource):

    def post(self):
        data = parser_2.parse_args()
        if(data['email']=="" and data['password1']!="" and data['password2']!=""):
            return "email address not given",400
        
        elif(data['email']=="" and data['password1']=="" and data['password2']==""):
            return "you have not entered any details",400
        
        elif(data['email']!="" and data['password1']=="" and data['password2']!=""):
            return "password missing",400
        
        elif(data['email']!="" and data['password1']!="" and data['password2']==""):
            return "second password missing",400
        
        #if UserModel.find_by_email(data['email']):
            #return {'message': 'User already exists'},409
        #new_user = UserModel(
            #email = data['email'],
            #password = UserModel.generate_hash(data['password'])
        #)
        try:
            #new_user.save_to_db()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            #return {
                #'message': 'User {} was created'.format(data['email']),
                #'access_token': access_token,
                #'refresh_token': refresh_token
               # },201
            return  'you have signed up in succesfully',201    
        except:
            return  'Something went wrong', 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return  'Access token has been revoked',200
        except:
            return 'Something went wrong', 500

    def get():
        pass

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return 'Refresh token has been revoked'
        except:
            return 'Something went wrong', 500
        
class getrequests(Resource):

    def get(self):
        
        pass
    
class getrequest(Resource):

    def get(self,req_id):
        
        
        pass

class editrequest(Resource):

    def editrequest(self):
        pass

class deleterequest(Resource):

    def get(self,req_id):
        pass
        

class createrequest(Resource):

    def post(self):
        pass

class resolveRequest(Resource):

    def post(self,req_id):
        pass
                
class approveRequest(Resource):

    def post(self,req_id):
        pass

class disapproveRequest(Resource):

    def post(self,req_id):
        pass

class getAllRequests(Resource):

    def get(self):
        pass
                

api.add_resource(myIndex, '/')        
api.add_resource(login, '/login')
api.add_resource(signup, '/signup')
api.add_resource(logout, '/logout')
api.add_resource(createrequest, '/createrequest')
api.add_resource(getrequest, '/getrequest/<string:req_id>')
api.add_resource(getrequests, '/getrequests/<string:email>')
api.add_resource(editrequest, '/editrequest/<string:req_id>')
api.add_resource(deleterequest, '/deleterequest/<string:req_id>')

#admin endpoints
api.add_resource(approveRequest, '/approveRequest/<string:req_id>')
api.add_resource(disapproveRequest, '/disapproveRequest/<string:req_id>')
api.add_resource(resolveRequest, '/resolveRequest/<string:req_id>')
api.add_resource(getAllRequests, '/getAllRequests')



