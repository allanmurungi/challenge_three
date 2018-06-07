from app import app
from app.DbHelper import DbCalls
from flask import jsonify,json
from flask_restful import Resource, Api, reqparse
from app.models import UserModel,RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import random



parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password1', help = 'This field cannot be blank', required = True)

Request_parser = reqparse.RequestParser()
Request_parser.add_argument('req_title', help = 'This field cannot be blank', required = True)
Request_parser.add_argument('req_details', help = 'This field cannot be blank', required = True)
Request_parser.add_argument('req_owner', help = 'This field cannot be blank', required = True)
Request_parser.add_argument('req_status', help = 'This field cannot be blank', required = True)



api = Api(app)



class myrequest:
    """ A template class for the request object """
    def __init__(self,req_title,req_details,req_owner):
        """ the constructor"""
        self.title=req_title
        self.details=req_details
        self.req_owner=req_owner
        self.req_status="null"
     
    
    def getreqtitle(self):
        return self.title

    def getreqdetails(self):
        return self.details

    def getreqemail(self):
        return self.req_owner

    

class myIndex(Resource):
    def get(self):
        return jsonify({'message': 'maintenance tracker endpoints!'});
    def post(self):
        return jsonify({'message': 'maintenance tracker endpoints post!'});


class login(Resource):
    def post(self):
        """ a  function for logging in a user given a provided email and password """

        data = parser.parse_args()
        
        if(UserModel.validate_login(data['email'],data['password1']) != True):
            return  json.dumps(UserModel.validate_login(data['email'],data['password1'])),400
           
        
        
        dbcall=DbCalls()
        con_status=dbcall.connect_to_db()
            
        access_token = create_access_token(identity = data['email'])
        refresh_token = create_refresh_token(identity = data['email'])
            
        if(con_status==True):

            

            return json.dumps({
        'message': 'you have logged in succesfully',
        'access_token':'',
        'refresh_token':''
        
        }),200 
        else:
            return  json.dumps({'message': 'you have failed to connect'}),500  
        
        return json.dumps({'message': 'Wrong credentials'}), 401


class signup(Resource):

    def post(self):
        """ a  function for creating a user given a provided email and password """

        data = parser.parse_args()
        if(UserModel.validate_signup(data['email'],data['password1']) != True):
            return  json.dumps(UserModel.validate_login(data['email'],data['password1'])),400
        
        
        
        dbcall=DbCalls()
        con_status=dbcall.connect_to_db()
            
        access_token = create_access_token(identity = data['email'])
        refresh_token = create_refresh_token(identity = data['email'])
            
        #get the email address and hash the password
        email=data['email']
        password=UserModel.generate_hash(data['password1'])

        #get user by username and return the user
        #verify hashed password using UserModel.verify_hash(data['password'], password_from_database
        if(con_status==True):

            dbcall.create_new_user(email,password,'user')
            dbcall.kill_connection()

            return json.dumps({
                    'message': 'you have signed up in succesfully',
                    'access_token':'',
                    'refresh_token':''
                }),201
        else:
            return json.dumps({'message': 'Something went wrong'}), 500    
        
        return json.dumps({'message': 'Something went wrong'}), 500

class signup_admin(Resource):

    def post(self):
        """ a  function for creating a user given a provided email and password """

        data = parser.parse_args()
        if(UserModel.validate_signup(data['email'],data['password1']) != True):
            return  json.dumps(UserModel.validate_login(data['email'],data['password1'])),400
        
        
        try:
            dbcall=DbCalls()
            con_status=dbcall.connect_to_db()
            
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            
            #get the email address and hash the password
            email=data['email']
            password=UserModel.generate_hash(data['password1'])

            #get user by username and return the user
            #verify hashed password using UserModel.verify_hash(data['password'], password_from_database
            if(con_status==True):

                dbcall.create_new_user(email,password,'admin')
                dbcall.kill_connection()

                return json.dumps({
                    'message': 'you have signed up in succesfully',
                    'access_token':'',
                    'refresh_token':''
                }),201
            else:
                return json.dumps({'message': 'Something went wrong'}), 500    
        except:
            return json.dumps({'message': 'Something went wrong'}), 500




class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """ a  function for refreshing token"""

        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class logout(Resource):
    @jwt_required
    def post(self):
        """ a  function for logging out a user  """

        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return json.dumps({'message': 'Access token has been revoked'}),200
        except:
            return json.dumps({'message': 'Something went wrong'}), 500

    def get(self):
        pass

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return json.dumps({'message': 'Refresh token has been revoked'})
        except:
            return json.dumps({'message': 'Something went wrong'}), 500
        
class getrequests(Resource):

    def get(self):
        """ a  function for getting requests for a user """
        
        pass
    
class getrequest(Resource):

    def get(self,req_id):
        """ a  function for getting a specific request """
        
        
        pass

class editrequest(Resource):

    def editrequest(self):
        """ a  function for editing/modifying a specific request """
        pass

class deleterequest(Resource):

    def get(self,req_id):
        """ a  function for deleting a specific request """
        pass
        

class createrequest(Resource):

    def post(self):
        """ a  function for creating a new request """

        #get parsed data
        data = Request_parser.parse_args()
        req_title=data['req_title']
        req_details=data['req_details']
        req_owner=data['req_owner']
        req_status=data['req_status']

        #validate each entry
        if(UserModel.validate_req(req_title) != True):
            return  json.dumps(UserModel.validate_req(req_title)),400
        elif(UserModel.validate_req(req_details) != True):
            return  json.dumps(UserModel.validate_req(req_details)),400
        elif(UserModel.validate_req(req_owner) != True):
            return  json.dumps(UserModel.validate_req(req_owner)),400
        elif(UserModel.validate_req(req_status) != True):
            return  json.dumps(UserModel.validate_req(req_status)),400 

        dbcall=DbCalls()
        con_status=dbcall.connect_to_db()
            
        #get user by username and return the user
        #verify hashed password using UserModel.verify_hash(data['password'], password_from_database
        if(con_status==True):

            dbcall.add_request(req_title,req_details,req_owner,req_status)
            dbcall.kill_connection()

            return json.dumps({
                    'message': 'request successfully added',
                }),201   
class resolveRequest(Resource):

    def post(self,req_id):
        """ a  function for resolving a specific request """
        pass
                
class approveRequest(Resource):

    def post(self,req_id):
        """ a  function for approving a specific request """
        pass

class disapproveRequest(Resource):

    def post(self,req_id):
        """ a  function for disapproving a specific request """
        pass

class getAllRequests(Resource):

    def get(self):
        """ a  function for getting all requests on the application """
        pass
                

api.add_resource(myIndex, '/')        
api.add_resource(login, '/login')
api.add_resource(signup, '/signup')
api.add_resource(signup_admin, '/signup_admin')
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



