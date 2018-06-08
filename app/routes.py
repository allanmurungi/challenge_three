from app import app
from app.DbHelper import DbCalls
from flask import jsonify, json
from flask_restful import Resource, Api, reqparse
from app.models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import random

parser = reqparse.RequestParser()
parser.add_argument('email', help='field cannot be blank', required=True)
parser.add_argument('password1', help='field cant be blank', required=True)

Request_parser = reqparse.RequestParser()
Request_parser.add_argument('req_title', help='cannot be blank', required=True)
Request_parser.add_argument('req_details', help='cant be blank', required=True)
Request_parser.add_argument('req_owner', help='blank field', required=True)
Request_parser.add_argument('req_status', help='blank field', required=True)

Edit_parser = reqparse.RequestParser()
Edit_parser.add_argument('req_id', help='field cannot be blank', required=True)
Edit_parser.add_argument('req_title', help='field is blank', required=True)
Edit_parser.add_argument('req_details', help='field is blank', required=True)
Edit_parser.add_argument('req_owner', help='field is blank', required=True)
Edit_parser.add_argument('req_status', help='field is blank', required=True)

api = Api(app)


class myrequest:

    """ A template class for the request object """

    def __init__(self, req_title, req_details, req_owner):
        """ the constructor"""
        self.title = req_title
        self.details = req_details
        self.req_owner = req_owner
        self.req_status = "null"

    def getreqtitle(self):
        return self.title

    def getreqdetails(self):
        return self.details

    def getreqemail(self):
        return self.req_owner


class myIndex(Resource):

    def get(self):
        return 'maintenance tracker endpoints!'

    def post(self):
        return 'maintenance tracker endpoints post!'


class login(Resource):

    def post(self):
        """ a  function for logging in a user given a provided email and password """
        data = parser.parse_args()

        if(UserModel.validate_login(data['email'], data['password1']) is not True):
            return UserModel.validate_login(data['email'], data['password1']), 400

        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()
        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])

        if(con_status is True):

            result = dbcall.log_in_user(data['email'], data['password1'])

            if UserModel.verify_hash(data['password1'], result[1]):
                return {
                    'message': 'you have logged in succesfully', 
                    'access_token': '', 
                    'refresh_token': ''}
            else:
                return {"message": "wrong credentials"}, 401    
        else:
            return {"message": "wrong credentials"}, 401


class signup(Resource):

    def post(self):
        """ a  function for creating a user given an email and password """

        data = parser.parse_args()
        if(UserModel.validate_signup(data['email'], data['password1']) is not True):
            return UserModel.validate_signup(data['email'], data['password1']), 400

        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()
        user_exists = dbcall.check_existing_user(data['email'])

        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])

        # get the email address and hash the password
        email = data['email']
        password = UserModel.generate_hash(data['password1'])

        # get user by username and return the user
        # verify hashed password , password_from_database
        if(con_status is True and user_exists is False):

            dbcall.create_new_user(email, password, 'user')
            dbcall.kill_connection()

            return {
                'message': 'you have signed up in succesfully',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        else:
            return {'message': 'user exists'}, 400

        return {'message': 'Something went wrong'}, 400


class signup_admin(Resource):

    def post(self):
        """ a  function for creating a user given a provided email and password """

        data = parser.parse_args()
        if(UserModel.validate_signup(data['email'], data['password1']) is not True):
            return UserModel.validate_signup(data['email'], data['password1']), 400

        try:
            dbcall = DbCalls()
            con_status = dbcall.connect_to_db()
            user_exists = dbcall.check_existing_user(data['email'])

            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])

            # get the email address and hash the password
            email = data['email']
            password = UserModel.generate_hash(data['password1'])

            # get user by username and return the user
            # verify hashed password using UserModel.verify_hash(data['password'], password_from_database
            if(con_status is True and user_exists is False):

                dbcall.create_new_user(email, password, 'admin')
                dbcall.kill_connection()

                return {
                    'message': 'you have signed up in succesfully',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 201
            else:
                return {'message': 'Something went wrong'}, 500
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """ a  function for refreshing token"""

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class logout(Resource):
    @jwt_required
    def post(self):
        """ a  function for logging out a user  """

        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()

            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        pass


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()

            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class getrequests(Resource):

    def get(self, email):
        """ a  function for getting requests for a user """

        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status is True):
            result = dbcall.get_user_requests(email)
            return result, 200


class getrequest(Resource):

    def get(self, req_id):
        """ a  function for getting a specific request """

        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            result = dbcall.get_request(req_id)
            return result, 200


class editrequest(Resource):

    def post(self):
        """ a  function for editing/modifying a specific request """
        data = Edit_parser.parse_args()

        req_id = data['req_id']
        req_title = data['req_title']
        req_details = data['req_details']
        req_owner = data['req_owner']
        req_status = data['req_status']

        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            result = dbcall.edit_request(
                req_title, req_details, req_owner, req_status, req_id)

        dbcall.kill_connection()
        return {"message":"request edited successfully"}, 200


class deleterequest(Resource):

    def get(self, req_id):
        """ a  function for deleting a specific request """
        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            result = dbcall.delete_request(req_id)

        dbcall.kill_connection()
        return {"message":"request deleted successfully"}, 200


class createrequest(Resource):

    def post(self):
        """ a  function for creating a new request """

        # get parsed data
        data = Request_parser.parse_args()
        req_title = data['req_title']
        req_details = data['req_details']
        req_owner = data['req_owner']
        req_status = data['req_status']

        # validate each entry
        if(UserModel.validate_req(req_title) is not True):
            return UserModel.validate_req(req_title), 400
        elif(UserModel.validate_req(req_details) is not True):
            return UserModel.validate_req(req_details), 400
        elif(UserModel.validate_email(req_owner) is not True):
            return UserModel.validate_req(req_owner), 400
        elif(UserModel.validate_req(req_status) is not True):
            return UserModel.validate_req(req_status), 400

        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        # get user by username and return the user
        # verify hashed password using UserModel.verify_hash(data['password'], password_from_database
        if(con_status == True):

            dbcall.add_request(req_title, req_details, req_owner, req_status)
            dbcall.kill_connection()

            return {
                'message': 'request successfully added',
            }, 201


class resolveRequest(Resource):

    def get(self, req_id):
        """ a  function for resolving a specific request """
        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            dbcall.resolve_request(req_id)
            dbcall.kill_connection()
            return {"message":"request resolved successfully"}, 200


class approveRequest(Resource):
    @jwt_required
    def get(self, req_id):
        """ a  function for approving a specific request """
        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            dbcall.approve_request(req_id)
        dbcall.kill_connection()
        return {"message":"request approved successfully"}, 200


class disapproveRequest(Resource):
    @jwt_required
    def get(self, req_id):
        """ a  function for disapproving a specific request """
        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            dbcall.disapprove_request(req_id)

        dbcall.kill_connection()
        return {"message":"request disapproved successfully"}, 200


class getAllRequests(Resource):
    @jwt_required
    def get(self):
        """ a  function for getting all requests on the application """
        dbcall = DbCalls()
        con_status = dbcall.connect_to_db()

        if(con_status == True):
            result = dbcall.get_all_requests()
            dbcall.kill_connection()
            return result, 200


api.add_resource(myIndex, '/')
api.add_resource(TokenRefresh, '/tokenrefresh')
api.add_resource(login, '/login')
api.add_resource(signup, '/signup')
api.add_resource(signup_admin, '/signup_admin')
api.add_resource(logout, '/logout')
api.add_resource(createrequest, '/createrequest')
api.add_resource(getrequest, '/getrequest/<string:req_id>')
api.add_resource(getrequests, '/getrequests/<string:email>')
api.add_resource(editrequest, '/editrequest')
api.add_resource(deleterequest, '/deleterequest/<string:req_id>')

# admin endpoints
api.add_resource(approveRequest, '/approveRequest/<string:req_id>')
api.add_resource(disapproveRequest, '/disapproveRequest/<string:req_id>')
api.add_resource(resolveRequest, '/resolveRequest/<string:req_id>')
api.add_resource(getAllRequests, '/getAllRequests')
